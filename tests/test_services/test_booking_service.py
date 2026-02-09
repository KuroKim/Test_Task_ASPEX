import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

# Трюк для импорта app
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.booking_service import BookingService
from app.models.booking import Booking


@pytest.mark.asyncio
@pytest.mark.parametrize("booking_time, is_valid", [
    (datetime(2026, 2, 10, 11, 59), False),  # Рано
    (datetime(2026, 2, 10, 12, 0), True),  # ОК
    (datetime(2026, 2, 10, 19, 59), True),  # ОК
    (datetime(2026, 2, 10, 20, 0), False),  # Поздно (закрытие в 22:00, слот 2 часа)
    (datetime(2026, 2, 10, 22, 0), False),  # Закрыто
])
async def test_booking_time_validation(booking_time, is_valid):
    # 1. Мокаем сессию БД
    mock_db = AsyncMock()

    # 2. Инициализируем сервис
    service = BookingService(db=mock_db)

    # 3. Подменяем репозитории внутри сервиса на Mock-объекты
    service.table_repo = AsyncMock()
    service.booking_repo = AsyncMock()

    # Создаем фейковый объект стола с нужным ID
    mock_table = MagicMock()
    mock_table.id = 1
    service.table_repo.get_available_tables.return_value = [mock_table]

    # Настраиваем поведение booking_repo: возвращает фейковый объект брони
    fake_booking = Booking(id="123", user_id="1", table_id=1)
    service.booking_repo.create.return_value = fake_booking

    # 4. Самое сложное: UserRepository создается внутри метода.
    # Используем patch, чтобы подменить класс UserRepository
    with patch("app.services.booking_service.UserRepository") as MockUserRepoClass:
        # Настраиваем мок: когда создается репо, у него есть метод get_by_id
        mock_user_repo_instance = AsyncMock()
        MockUserRepoClass.return_value = mock_user_repo_instance

        # Метод get_by_id возвращает объект с email (чтобы Celery не упал)
        mock_user = MagicMock()
        mock_user.email = "test@test.com"
        mock_user_repo_instance.get_by_id.return_value = mock_user

        # --- ЗАПУСК ТЕСТА ---
        if is_valid:
            # Если время валидно, ожидаем успешное выполнение
            result = await service.create_booking(user_id=1, table_id=1, start_time=booking_time)
            assert result == fake_booking
        else:
            # Если время НЕ валидно, ожидаем ошибку
            with pytest.raises(ValueError):
                await service.create_booking(user_id=1, table_id=1, start_time=booking_time)
