from typing import List
from datetime import datetime
from sqlalchemy import select, and_, not_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.table import Table
from app.models.booking import Booking
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    def __init__(self, session: AsyncSession):
        super().__init__(Table, session)

    async def get_available_tables(self, start_time: datetime, end_time: datetime) -> List[Table]:
        """
        Retrieves tables that do not have overlapping bookings in the given time range.
        Intersection logic: (StartA < EndB) and (EndA > StartB)
        """
        # Subquery to find IDs of occupied tables
        busy_tables_subquery = select(Booking.table_id).where(
            and_(
                Booking.booking_start < end_time,
                Booking.booking_end > start_time
            )
        )

        # Select tables not present in the busy list
        query = select(Table).where(
            not_(Table.id.in_(busy_tables_subquery))
        )

        result = await self.session.execute(query)
        return result.scalars().all()
