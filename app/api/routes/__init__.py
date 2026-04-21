from app.api.routes.auth import router as auth_router
from app.api.routes.projects import router as projects_router
from app.api.routes.web import router as web_router

__all__ = ["auth_router", "projects_router", "web_router"]
