import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.session import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .table import Table


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"), nullable=False)

    booking_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    booking_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Связи
    user: Mapped["User"] = relationship(back_populates="bookings")
    table: Mapped["Table"] = relationship(back_populates="bookings")
