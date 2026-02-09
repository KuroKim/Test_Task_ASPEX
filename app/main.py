import sys
from fastapi import FastAPI
from loguru import logger

from app.core.config import settings
from app.api.api import api_router

# --- Logging Configuration ---
# Remove default handler and add a structured one
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO"
)
# Optional: Add file logging
# logger.add("logs/app.log", rotation="10 MB", level="INFO")
# -----------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    logger.info("Root health check endpoint accessed")
    return {"message": "Restaurant Booking API is running!"}
