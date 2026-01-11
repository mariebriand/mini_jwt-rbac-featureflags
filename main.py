from fastapi import FastAPI

from app.api.routers.health import router as health_router

app = FastAPI(
    title="Mini Auth Service",
    version="0.1.0",
)

@app.get("/")
async def hello():
    return {"message": "Hello World!"}

app.include_router(health_router)