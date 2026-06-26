from workers import WorkerEntrypoint

from app.config import sync_worker_env
from app.main import app


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        sync_worker_env(self.env)
        try:
            import asgi
            return await asgi.fetch(app, request.js_object, self.env)
        except Exception as exc:
            import json
            print(json.dumps({"event": "worker_crash", "error_type": exc.__class__.__name__, "error_message": str(exc)}))
            raise
