import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class BookingBase(BaseModel):
    table_id: int
    booking_start: datetime

    # Валидатор: время должно быть в будущем (простая проверка)
    @field_validator('booking_start')
    def validate_future(cls, v):
        if v.replace(tzinfo=None) < datetime.now():
            raise ValueError('Время бронирования должно быть в будущем')
        return v


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    id: uuid.UUID
    user_id: uuid.UUID
    booking_end: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
