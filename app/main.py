from fastapi import FastAPI

from app.config.settings import settings
from app.db.init_db import init_db

from app.api.routers.health import router as health_router
from app.api.routers.user import router as user_router
from app.api.routers.auth import router as auth_router

init_db()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/")
async def hello():
    return {"message": settings}


app.include_router(health_router)

# Include routers
app.include_router(user_router)
app.include_router(auth_router)
