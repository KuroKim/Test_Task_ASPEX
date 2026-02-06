from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db

    async def register_new_user(self, user_in: UserCreate) -> User:
        """Регистрация пользователя: проверка email + хеширование пароля"""
        # Проверяем, не занят ли email
        existing_user = await self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Подготавливаем данные (заменяем сырой пароль на хеш)
        user_data = user_in.model_dump()
        password = user_data.pop("password")
        user_data["hashed_password"] = get_password_hash(password)

        # Создаем через репозиторий
        new_user = await self.user_repo.create(user_data)
        await self.db.commit()  # Фиксируем изменения в базе
        return new_user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Проверка логина/пароля"""
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
