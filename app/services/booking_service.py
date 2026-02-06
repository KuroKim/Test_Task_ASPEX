from datetime import datetime, timedelta
from typing import List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.booking_repo import BookingRepository
from app.repositories.table_repo import TableRepository
from app.models.booking import Booking
from app.models.table import Table


class BookingService:
    def __init__(self, db: AsyncSession):
        self.booking_repo = BookingRepository(db)
        self.table_repo = TableRepository(db)
        self.db = db

    async def create_booking(self, user_id: uuid.UUID, table_id: int, start_time: datetime) -> Booking:
        # 1. Проверяем рабочие часы (12:00 - 22:00)
        # В ТЗ сказано: закрытие в 22:00. Т.к. бронь на 2 часа,
        # последнее время начала брони — 20:00.
        if not (12 <= start_time.hour < 20):
            raise ValueError("Restaurant is open for bookings from 12:00 to 20:00 (closes at 22:00)")

        # 2. Вычисляем время окончания (фиксированно 2 часа)
        end_time = start_time + timedelta(hours=2)

        # 3. Проверяем, свободен ли конкретный стол
        available_tables = await self.table_repo.get_available_tables(start_time, end_time)
        if table_id not in [t.id for t in available_tables]:
            raise ValueError("Table is already booked for this time")

        # 4. Создаем бронь
        booking_data = {
            "user_id": user_id,
            "table_id": table_id,
            "booking_start": start_time,
            "booking_end": end_time
        }
        new_booking = await self.booking_repo.create(booking_data)
        await self.db.commit()
        return new_booking

    async def get_available_tables_for_time(self, start_time: datetime) -> List[Table]:
        """Поиск всех свободных столов на конкретное время"""
        end_time = start_time + timedelta(hours=2)
        return await self.table_repo.get_available_tables(start_time, end_time)
