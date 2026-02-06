from sqlalchemy.ext.asyncio import AsyncSession
from app.models.booking import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    # Тут можно добавить специфичные методы, например "получить брони юзера"
