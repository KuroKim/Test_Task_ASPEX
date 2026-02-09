from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from app.db.session import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .booking import Booking


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)  # Like "Table 1"
    capacity: Mapped[int] = mapped_column(Integer)  # 2, 3, 6

    # Связь
    bookings: Mapped[List["Booking"]] = relationship(back_populates="table")
