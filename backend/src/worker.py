from workers import WorkerEntrypoint, Response

from app.config import sync_worker_env
from app.main import app

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        if request.method == "OPTIONS":
            return Response(None, headers=CORS_HEADERS, status=204)

        sync_worker_env(self.env)
        try:
            import asgi
            return await asgi.fetch(app, request.js_object, self.env)
        except Exception as exc:
            import json
            print(json.dumps({"event": "worker_crash", "error_type": exc.__class__.__name__, "error_message": str(exc)}))
            return Response(
                json.dumps({"detail": "Internal server error"}),
                headers={"Content-Type": "application/json", **CORS_HEADERS},
                status=500,
            )
