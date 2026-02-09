import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """
    Base user schema with common fields.
    """
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user registration, including password.
    """
    password: str


class UserRead(UserBase):
    """
    Schema for user data output, strictly excluding password hash.
    """
    id: uuid.UUID
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)
