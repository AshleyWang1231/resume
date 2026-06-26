from workers import WorkerEntrypoint

from app.config import sync_worker_env
from app.main import app


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        sync_worker_env(self.env)
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)
