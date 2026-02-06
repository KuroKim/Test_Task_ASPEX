from fastapi import FastAPI
from app.core.config import settings
from app.api.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# Подключаем все наши роуты
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Restaurant Booking API is running!"}
