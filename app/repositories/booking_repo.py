from typing import Optional, List
import uuid
from sqlalchemy import select
from app.models.booking import Booking
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session):
        super().__init__(Booking, session)

    async def get_by_user(self, user_id: uuid.UUID) -> List[Booking]:
        """
        Retrieves all bookings for a specific user.
        """
        query = select(Booking).where(Booking.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id_and_user(self, booking_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Booking]:
        """
        Finds a specific booking for a user (ensures ownership).
        """
        query = select(Booking).where(
            Booking.id == booking_id,
            Booking.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
