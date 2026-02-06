from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Создаем асинхронный движок
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,  # Логирует все SQL запросы (удобно для отладки, в проде отключить)
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# Dependency для FastAPI (будем использовать в роутах)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
