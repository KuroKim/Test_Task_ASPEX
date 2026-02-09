from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,  # Set to False in production to disable SQL logging
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


# Base class for declarative models
class Base(DeclarativeBase):
    pass


# FastAPI dependency for database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
