# app/routers/__init__.py
from app.routers.farmers import router as farmers_router
from app.routers.auth import router as auth_router
from app.routers.loans import router as loans_router
from app.routers.dashboard import router as dashboard_router
from app.routers.ai import router as ai_router

__all__ = [
    "farmers_router",
    "auth_router",
    "loans_router",
    "dashboard_router",
    "ai_router",
]