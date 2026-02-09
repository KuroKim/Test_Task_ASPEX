import sys
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings
from app.api.api import api_router

# ---- НАСТРОЙКА ЛОГГЕРА ----
# Удаляем стандартный обработчик
logger.remove()
# Добавляем новый, который пишет в stderr
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
# Можно добавить запись в файл
# logger.add("logs/app.log", rotation="10 MB", level="INFO")
# -----------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root endpoint was called")
    return {"message": "Restaurant Booking API is running!"}
