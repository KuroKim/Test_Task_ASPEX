import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class BookingBase(BaseModel):
    table_id: int
    booking_start: datetime

    @field_validator('booking_start')
    def validate_future(cls, v):
        """
        Ensures the booking date is set in the future.
        """
        if v.replace(tzinfo=None) < datetime.now():
            raise ValueError('Booking time must be in the future')
        return v


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: uuid.UUID
    user_id: uuid.UUID
    booking_end: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
