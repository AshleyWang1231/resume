import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from app.main import app
from asgiref.wsgi import WsgiToAsgi
import io
import json
import asyncio
import urllib.parse


def handler(environ, start_response):
    """Aliyun FC3 python3.10 HTTP handler — wraps FastAPI via ASGI."""
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(_handle_asgi(environ))
    finally:
        loop.close()

    status, headers, body = result
    start_response(status, headers)
    return [body]


async def _handle_asgi(environ):
    method = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    query_string = environ.get("QUERY_STRING", "")
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    body = environ["wsgi.input"].read(content_length) if content_length else b""

    headers = {}
    for key, value in environ.items():
        if key.startswith("HTTP_"):
            header_name = key[5:].replace("_", "-").lower()
            headers[header_name] = value
        elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            header_name = key.replace("_", "-").lower()
            headers[header_name] = value

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "headers": [(k.encode(), v.encode()) for k, v in headers.items()],
        "path": path,
        "query_string": query_string.encode(),
        "root_path": "",
        "scheme": "https",
        "server": ("localhost", 9000),
    }

    response_started = {}
    response_body = io.BytesIO()

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        if message["type"] == "http.response.start":
            response_started["status"] = message["status"]
            response_started["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response_body.write(message.get("body", b""))

    await app(scope, receive, send)

    status_code = response_started.get("status", 500)
    raw_headers = response_started.get("headers", [])
    headers_list = [(k.decode(), v.decode()) for k, v in raw_headers]
    body_bytes = response_body.getvalue()

    status_str = f"{status_code} {_status_phrase(status_code)}"
    return status_str, headers_list, body_bytes


def _status_phrase(code):
    phrases = {200: "OK", 204: "No Content", 400: "Bad Request", 404: "Not Found",
               422: "Unprocessable Entity", 500: "Internal Server Error", 503: "Service Unavailable"}
    return phrases.get(code, "Unknown")
