from typing import List
from datetime import datetime
from sqlalchemy import select, and_, not_, exists
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.table import Table
from app.models.booking import Booking
from app.repositories.base import BaseRepository


class TableRepository(BaseRepository[Table]):
    def __init__(self, session: AsyncSession):
        super().__init__(Table, session)

    async def get_available_tables(self, start_time: datetime, end_time: datetime) -> List[Table]:
        """
        Самый сложный запрос: найти столы, у которых НЕТ пересекающихся броней.
        """
        # Подзапрос: найти ID столов, которые заняты в этот промежуток
        # Пересечение интервалов: (StartA < EndB) and (EndA > StartB)
        busy_tables_subquery = select(Booking.table_id).where(
            and_(
                Booking.booking_start < end_time,
                Booking.booking_end > start_time
            )
        )

        # Основной запрос: выбрать столы, ID которых НЕТ в списке занятых
        query = select(Table).where(
            not_(Table.id.in_(busy_tables_subquery))
        )

        result = await self.session.execute(query)
        return result.scalars().all()
