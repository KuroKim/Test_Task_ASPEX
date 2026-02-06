import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# Базовый класс (общие поля)
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


# Схема для создания (то, что шлет клиент при регистрации)
class UserCreate(UserBase):
    password: str


# Схема для чтения (то, что мы отдаем клиенту)
# Важно: тут НЕТ пароля!
class UserRead(UserBase):
    id: uuid.UUID
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
