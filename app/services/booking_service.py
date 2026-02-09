import uuid
from datetime import datetime, timedelta, timezone
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
        """
        Creates a new booking after validating business rules.

        - Checks if the booking time is within restaurant operating hours.
        - Verifies that the requested table is available for the 2-hour slot.
        - Triggers an asynchronous email confirmation task upon success.

        Args:
            user_id: The ID of the user creating the booking.
            table_id: The ID of the table to book.
            start_time: The desired start time for the booking.

        Returns:
            The newly created Booking object.

        Raises:
            ValueError: If a business rule is violated (e.g., table is booked).
        """
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

    async def delete_booking(self, booking_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """
        Cancels a booking if it's more than 1 hour before the start time.
        """
        booking = await self.booking_repo.get_by_id_and_user(booking_id, user_id)

        if not booking:
            raise ValueError("Booking not found or you don't have permission to delete it")

        # Проверка времени: сейчас + 1 час должно быть меньше, чем начало брони
        if datetime.now(timezone.utc) + timedelta(hours=1) > booking.booking_start:
            raise ValueError("Cancellations are only allowed at least 1 hour before the booking starts")

        await self.booking_repo.delete(booking_id)
        await self.db.commit()

    async def get_user_bookings(self, user_id: uuid.UUID) -> List[Booking]:
        """Returns all bookings for a specific user"""
        return await self.booking_repo.get_by_user(user_id)

    async def get_available_tables_for_time(self, start_time: datetime) -> List[Table]:
        """Поиск всех свободных столов на конкретное время"""
        end_time = start_time + timedelta(hours=2)
        return await self.table_repo.get_available_tables(start_time, end_time)
