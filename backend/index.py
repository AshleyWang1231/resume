import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

import io
import json
import asyncio

from app.main import app


def handler(event, context):
    """Aliyun FC3 python3.10 HTTP trigger handler."""
    if isinstance(event, (bytes, bytearray)):
        raw = event.decode("utf-8")
    else:
        raw = event

    print(f"RAW_EVENT: {raw[:500]}")

    try:
        evt = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        evt = {}

    # FC HTTP trigger v2 format uses 'requestContext', 'rawPath', 'rawQueryString'
    # FC HTTP trigger v1 format uses 'httpMethod', 'path', 'queryString'
    if "requestContext" in evt:
        method = evt.get("requestContext", {}).get("http", {}).get("method", "GET")
        path = evt.get("rawPath", "/")
        query_string = evt.get("rawQueryString", "")
        raw_headers = evt.get("headers") or {}
        body_str = evt.get("body") or ""
        is_base64 = evt.get("isBase64Encoded", False)
    else:
        method = evt.get("httpMethod") or evt.get("method", "GET")
        path = evt.get("path", "/")
        query_string = evt.get("queryString") or ""
        if isinstance(query_string, dict):
            query_string = "&".join(f"{k}={v}" for k, v in query_string.items())
        raw_headers = evt.get("headers") or {}
        body_str = evt.get("body") or ""
        is_base64 = evt.get("isBase64Encoded", False)

    if is_base64:
        import base64
        body_bytes = base64.b64decode(body_str)
    else:
        body_bytes = body_str.encode("utf-8") if isinstance(body_str, str) else body_str

    headers = [(k.lower().encode(), v.encode()) for k, v in raw_headers.items()]

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method.upper(),
        "headers": headers,
        "path": path,
        "query_string": query_string.encode(),
        "root_path": "",
        "scheme": "https",
        "server": ("localhost", 9000),
    }

    response_started = {}
    response_body = io.BytesIO()

    async def receive():
        return {"type": "http.request", "body": body_bytes, "more_body": False}

    async def send(message):
        if message["type"] == "http.response.start":
            response_started["status"] = message["status"]
            response_started["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response_body.write(message.get("body", b""))

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(app(scope, receive, send))
    finally:
        loop.close()

    status_code = response_started.get("status", 500)
    resp_headers = {k.decode(): v.decode() for k, v in response_started.get("headers", [])}
    body_out = response_body.getvalue()

    # Override FC trigger's forced Content-Disposition: attachment on HTML
    resp_headers["x-fc-status"] = str(status_code)
    if "content-disposition" not in resp_headers:
        resp_headers["content-disposition"] = "inline"

    return {
        "statusCode": status_code,
        "headers": resp_headers,
        "body": body_out.decode("utf-8", errors="replace"),
        "isBase64Encoded": False,
    }
