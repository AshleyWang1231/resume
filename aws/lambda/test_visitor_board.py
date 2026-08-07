import importlib.util
import json
import sys
import types
from pathlib import Path
from unittest.mock import Mock

sys.modules.setdefault("boto3", types.SimpleNamespace(resource=lambda service: None))

MODULE_PATH = Path(__file__).parent / "visitor_board.py"
spec = importlib.util.spec_from_file_location("visitor_board", MODULE_PATH)
visitor_board = importlib.util.module_from_spec(spec)
spec.loader.exec_module(visitor_board)


class FakeTable:
    def __init__(self):
        self.items = []

    def put_item(self, Item):
        self.items.append(Item)

    def scan(self, **kwargs):
        return {"Items": list(self.items)}

    def get_item(self, Key):
        for item in self.items:
            if item["id"] == Key["id"]:
                return {"Item": item}
        return {}

    def update_item(self, Key, UpdateExpression, ExpressionAttributeValues, ReturnValues):
        for item in self.items:
            if item["id"] == Key["id"]:
                item["message"] = ExpressionAttributeValues[":message"]
                return {"Attributes": item}
        return {}

    def delete_item(self, Key):
        self.items = [item for item in self.items if item["id"] != Key["id"]]


def event(method, body=None, path="/messages"):
    return {
        "rawPath": path,
        "requestContext": {"http": {"method": method}},
        "body": json.dumps(body) if body is not None else None,
    }


def test_create_and_list_message():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))

    created = visitor_board.lambda_handler(event("POST", {"name": "Hiring Manager", "message": "Great resume."}), None)
    assert created["statusCode"] == 201
    created_body = json.loads(created["body"])
    assert set(created_body["item"]) == {"id", "name", "message", "createdAt"}
    assert created_body["item"]["name"] == "Hiring Manager"
    assert created_body["item"]["message"] == "Great resume."

    listed = visitor_board.lambda_handler(event("GET"), None)
    assert listed["statusCode"] == 200
    listed_body = json.loads(listed["body"])
    assert len(listed_body["items"]) == 1
    assert listed_body["items"][0]["message"] == "Great resume."


def test_get_messages_sorts_before_limiting():
    table = FakeTable()
    table.items = [
        {"id": "1", "name": "A", "message": "old", "createdAt": "2026-08-06T10:00:00Z"},
        {"id": "2", "name": "B", "message": "new", "createdAt": "2026-08-06T12:00:00Z"},
        {"id": "3", "name": "C", "message": "middle", "createdAt": "2026-08-06T11:00:00Z"},
    ]
    visitor_board.MAX_MESSAGES = 2

    items = visitor_board.get_messages(table)

    assert [item["message"] for item in items] == ["new", "middle"]
    visitor_board.MAX_MESSAGES = 25


def test_rejects_empty_name():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))

    result = visitor_board.lambda_handler(event("POST", {"name": " ", "message": "Hello"}), None)
    assert result["statusCode"] == 400
    assert json.loads(result["body"])["error"] == "Name and message are required."


def test_rejects_non_object_json_body():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))

    result = visitor_board.lambda_handler(event("POST", ["not", "an", "object"]), None)

    assert result["statusCode"] == 400
    assert json.loads(result["body"])["error"] == "Request body must be a JSON object."


def test_options_has_cors_headers():
    result = visitor_board.lambda_handler(event("OPTIONS"), None)
    assert result["statusCode"] == 204
    assert result["headers"]["Access-Control-Allow-Methods"] == "GET,POST,PATCH,DELETE,OPTIONS"
    assert result["headers"]["Access-Control-Max-Age"] == "86400"

def test_create_returns_edit_token_but_get_redacts_internal_fields():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))

    created = visitor_board.lambda_handler(event("POST", {"name": "Owner", "message": "Editable"}), None)
    body = json.loads(created["body"])

    assert created["statusCode"] == 201
    assert body["editToken"]
    assert body["editExpiresAt"]
    stored = table.items[0]
    assert "editTokenHash" in stored
    assert "editToken" not in stored

    listed = visitor_board.lambda_handler(event("GET"), None)
    public_item = json.loads(listed["body"])["items"][0]
    assert set(public_item) == {"id", "name", "message", "createdAt"}


def test_patch_updates_message_with_valid_unexpired_token():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))
    created = visitor_board.lambda_handler(event("POST", {"name": "Owner", "message": "Original"}), None)
    body = json.loads(created["body"])
    message_id = body["item"]["id"]

    patched = visitor_board.lambda_handler(event("PATCH", {"message": "Updated", "editToken": body["editToken"]}, f"/messages/{message_id}"), None)

    assert patched["statusCode"] == 200
    assert json.loads(patched["body"])["item"]["message"] == "Updated"
    assert table.items[0]["message"] == "Updated"


def test_delete_removes_message_with_valid_unexpired_token():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))
    created = visitor_board.lambda_handler(event("POST", {"name": "Owner", "message": "Delete me"}), None)
    body = json.loads(created["body"])
    message_id = body["item"]["id"]

    deleted = visitor_board.lambda_handler(event("DELETE", {"editToken": body["editToken"]}, f"/messages/{message_id}"), None)

    assert deleted["statusCode"] == 200
    assert json.loads(deleted["body"])["ok"] is True
    assert table.items == []


def test_patch_rejects_invalid_token():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))
    created = visitor_board.lambda_handler(event("POST", {"name": "Owner", "message": "Original"}), None)
    message_id = json.loads(created["body"])["item"]["id"]

    patched = visitor_board.lambda_handler(event("PATCH", {"message": "Updated", "editToken": "wrong"}, f"/messages/{message_id}"), None)

    assert patched["statusCode"] == 403
    assert json.loads(patched["body"])["error"] == "Invalid edit token."


def test_delete_rejects_expired_token():
    table = FakeTable()
    visitor_board.dynamodb = Mock(Table=Mock(return_value=table))
    created = visitor_board.lambda_handler(event("POST", {"name": "Owner", "message": "Original"}), None)
    body = json.loads(created["body"])
    message_id = body["item"]["id"]
    table.items[0]["editExpiresAt"] = "2000-01-01T00:00:00Z"

    deleted = visitor_board.lambda_handler(event("DELETE", {"editToken": body["editToken"]}, f"/messages/{message_id}"), None)

    assert deleted["statusCode"] == 403
    assert json.loads(deleted["body"])["error"] == "Edit window has expired."
