import uuid
from datetime import datetime, timedelta
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.booking_repo import BookingRepository
from app.repositories.table_repo import TableRepository
from app.repositories.user_repo import UserRepository
from app.models.booking import Booking
from app.models.table import Table
from app.worker.tasks import send_booking_confirmation_email


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
        # Проверка: есть ли table_id среди ID свободных столов
        if table_id not in [t.id for t in available_tables]:
            raise ValueError(f"Table {table_id} is not available for this time")

        # 4. Создаем бронь
        booking_data = {
            "user_id": user_id,
            "table_id": table_id,
            "booking_start": start_time,
            "booking_end": end_time
        }
        new_booking = await self.booking_repo.create(booking_data)

        # 5. Получаем юзера для отправки письма
        user_repo = UserRepository(self.db)
        user = await user_repo.get_by_id(user_id)

        await self.db.commit()

        # 6. Отправляем задачу в Celery
        if user:
            send_booking_confirmation_email.delay(user.email, str(new_booking.id))

        return new_booking

    async def get_available_tables_for_time(self, start_time: datetime) -> List[Table]:
        """Поиск всех свободных столов на конкретное время"""
        end_time = start_time + timedelta(hours=2)
        return await self.table_repo.get_available_tables(start_time, end_time)
