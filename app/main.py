from fastapi import FastAPI

from app.core.config import settings
from app.db.init_db import init_db

from app.api.routers.health import router as health_router
from app.api.routers.user import router as user_router
from app.api.routers.authentication import router as authn_router
from app.api.routers.authorization import router as authz_router
from app.api.routers.feature_flag import router as flag_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
async def hello():
    return {
        "app_name": settings.app_name,
        "app_version": settings.app_version,
        "status": "OK",
        "message": "Hello World!",
    }


app.include_router(health_router)

# Include routers
app.include_router(user_router)
app.include_router(authn_router)
app.include_router(authz_router)
app.include_router(flag_router)
