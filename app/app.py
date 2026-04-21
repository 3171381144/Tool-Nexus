from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth_router, projects_router, web_router
from app.seed import bootstrap_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    bootstrap_database()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Portal Auth Service",
        description="用于内部工具聚合门户的 SSO 与 Forward Auth 服务",
        version="1.0.0",
        lifespan=lifespan,
    )

    @app.get("/healthz", tags=["system"])
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(web_router)
    app.include_router(auth_router, prefix="/api")
    app.include_router(projects_router, prefix="/api")
    return app
