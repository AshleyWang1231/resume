import hashlib
import hmac
import json
import logging
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "ResumeVisitorMessages")
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "25"))
EDIT_WINDOW_SECONDS = int(os.environ.get("EDIT_WINDOW_SECONDS", "180"))

PUBLIC_FIELDS = ("id", "name", "message", "createdAt")


def response(status_code, body=None, extra_headers=None):
    headers = {
        "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        "Access-Control-Allow-Methods": "GET,POST,PATCH,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    result = {
        "statusCode": status_code,
        "headers": headers,
    }
    if body is not None:
        result["body"] = json.dumps(body)
    return result


def now_utc():
    return datetime.now(timezone.utc)


def to_iso(value):
    return value.isoformat().replace("+00:00", "Z")


def parse_iso(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def public_item(item):
    return {key: item[key] for key in PUBLIC_FIELDS if key in item}


def parse_body(event):
    raw_body = event.get("body")
    if not raw_body:
        raise ValueError("Name and message are required.")
    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")
    return payload


def validate_message(payload, require_name=True):
    raw_name = payload.get("name", "")
    raw_message = payload.get("message", "")
    if (require_name and not isinstance(raw_name, str)) or not isinstance(raw_message, str):
        raise ValueError("Name and message must be text.")

    name = raw_name.strip()
    message = raw_message.strip()

    if require_name and not name:
        raise ValueError("Name and message are required.")
    if not message:
        raise ValueError("Name and message are required." if require_name else "Message must be between 1 and 500 characters.")
    if require_name and len(name) > 80:
        raise ValueError("Name must be 80 characters or fewer.")
    if len(message) > 500:
        raise ValueError("Message must be 500 characters or fewer.")

    return name, message


def get_messages(table):
    scan_result = table.scan()
    items = scan_result.get("Items", [])

    while "LastEvaluatedKey" in scan_result:
        scan_result = table.scan(ExclusiveStartKey=scan_result["LastEvaluatedKey"])
        items.extend(scan_result.get("Items", []))

    items.sort(key=lambda item: item.get("createdAt", ""), reverse=True)
    return [public_item(item) for item in items[:MAX_MESSAGES]]


def create_message(table, payload):
    name, message = validate_message(payload)
    edit_token = secrets.token_urlsafe(32)
    edit_expires_at = to_iso(now_utc() + timedelta(seconds=EDIT_WINDOW_SECONDS))
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "message": message,
        "createdAt": to_iso(now_utc()),
        "editTokenHash": hash_token(edit_token),
        "editExpiresAt": edit_expires_at,
    }
    table.put_item(Item=item)
    return public_item(item), edit_token, edit_expires_at


def message_id_from_path(path):
    prefix = "/messages/"
    if not path.startswith(prefix) or path == prefix:
        raise ValueError("Message id is required.")
    return path[len(prefix):].strip()


def get_existing_item(table, message_id):
    result = table.get_item(Key={"id": message_id})
    item = result.get("Item")
    if not item:
        raise LookupError("Message not found.")
    return item


def verify_edit_token(item, edit_token):
    if not edit_token:
        raise PermissionError("Edit token is required.")
    if parse_iso(item.get("editExpiresAt", "1970-01-01T00:00:00Z")) < now_utc():
        raise PermissionError("Edit window has expired.")
    if not hmac.compare_digest(item.get("editTokenHash", ""), hash_token(edit_token)):
        raise PermissionError("Invalid edit token.")


def update_message(table, message_id, payload):
    _, message = validate_message(payload, require_name=False)
    item = get_existing_item(table, message_id)
    verify_edit_token(item, str(payload.get("editToken", "")))
    updated = table.update_item(
        Key={"id": message_id},
        UpdateExpression="SET message = :message",
        ExpressionAttributeValues={":message": message},
        ConditionExpression="attribute_exists(id)",
        ReturnValues="ALL_NEW",
    )["Attributes"]
    return public_item(updated)


def delete_message(table, message_id, payload):
    item = get_existing_item(table, message_id)
    verify_edit_token(item, str(payload.get("editToken", "")))
    table.delete_item(Key={"id": message_id})


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("rawPath", "/")

    if method == "OPTIONS":
        return response(204, extra_headers={"Access-Control-Max-Age": "86400"})

    table = dynamodb.Table(TABLE_NAME)

    try:
        if method == "GET" and path.rstrip("/") == "/messages":
            return response(200, {"items": get_messages(table)})

        if method == "POST" and path.rstrip("/") == "/messages":
            item, edit_token, edit_expires_at = create_message(table, parse_body(event))
            return response(201, {"item": item, "editToken": edit_token, "editExpiresAt": edit_expires_at})

        if method == "PATCH":
            item = update_message(table, message_id_from_path(path), parse_body(event))
            return response(200, {"item": item})

        if method == "DELETE":
            delete_message(table, message_id_from_path(path), parse_body(event))
            return response(200, {"ok": True})

        if path.startswith("/messages"):
            return response(405, {"error": "Method not allowed."})
        return response(404, {"error": "Not found."})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except LookupError as exc:
        return response(404, {"error": str(exc)})
    except PermissionError as exc:
        return response(403, {"error": str(exc)})
    except Exception:
        logger.exception("Visitor Board request failed")
        return response(500, {"error": "Something went wrong. Please try again later."})
