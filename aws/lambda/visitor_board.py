import json
import logging
import os
import uuid
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "ResumeVisitorMessages")
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "*")
MAX_MESSAGES = int(os.environ.get("MAX_MESSAGES", "25"))


def response(status_code, body=None, extra_headers=None):
    headers = {
        "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
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


def parse_body(event):
    raw_body = event.get("body")
    if not raw_body:
        raise ValueError("Name and message are required.")
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def validate_message(payload):
    name = str(payload.get("name", "")).strip()
    message = str(payload.get("message", "")).strip()

    if not name or not message:
        raise ValueError("Name and message are required.")
    if len(name) > 80:
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
    return items[:MAX_MESSAGES]


def create_message(table, payload):
    name, message = validate_message(payload)
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "message": message,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    table.put_item(Item=item)
    return item


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("rawPath", "/")

    if method == "OPTIONS":
        return response(204, extra_headers={"Access-Control-Max-Age": "86400"})

    if path.rstrip("/") != "/messages":
        return response(404, {"error": "Not found."})

    table = dynamodb.Table(TABLE_NAME)

    try:
        if method == "GET":
            return response(200, {"items": get_messages(table)})

        if method == "POST":
            item = create_message(table, parse_body(event))
            return response(201, {"item": item})

        return response(405, {"error": "Method not allowed."})
    except ValueError as exc:
        return response(400, {"error": str(exc)})
    except Exception:
        logger.exception("Visitor Board request failed")
        return response(500, {"error": "Something went wrong. Please try again later."})
