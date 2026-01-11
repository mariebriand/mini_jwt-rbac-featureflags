from fastapi import FastAPI

from app.config.ettings import settings
from app.api.routers.health import router as health_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

@app.get("/")
async def hello():
    return {"message": "Starting app: "+settings.app_name}

app.include_router(health_router)