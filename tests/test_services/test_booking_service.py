import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

# Add project root to sys.path for proper imports
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.services.booking_service import BookingService
from app.models.booking import Booking


@pytest.mark.asyncio
@pytest.mark.parametrize("booking_time, is_valid", [
    (datetime(2026, 2, 10, 11, 59), False),  # Too early
    (datetime(2026, 2, 10, 12, 0), True),  # Opening time - OK
    (datetime(2026, 2, 10, 19, 59), True),  # Last slot - OK
    (datetime(2026, 2, 10, 20, 0), False),  # Too late (22:00 closing, 2h slot)
    (datetime(2026, 2, 10, 22, 0), False),  # Already closed
])
async def test_booking_time_validation(booking_time, is_valid):
    """
    Unit test to verify booking time business rules.
    """
    # 1. Mock DB session
    mock_db = AsyncMock()

    # 2. Initialize service
    service = BookingService(db=mock_db)

    # 3. Mock internal repositories
    service.table_repo = AsyncMock()
    service.booking_repo = AsyncMock()

    # Setup table_repo to return an available table
    mock_table = MagicMock()
    mock_table.id = 1
    service.table_repo.get_available_tables.return_value = [mock_table]

    # Setup booking_repo to return a fake booking object
    fake_booking = Booking(id="123", user_id="1", table_id=1)
    service.booking_repo.create.return_value = fake_booking

    # 4. Patch UserRepository which is instantiated inside the service method
    with patch("app.services.booking_service.UserRepository") as MockUserRepoClass:
        mock_user_repo_instance = AsyncMock()
        MockUserRepoClass.return_value = mock_user_repo_instance

        # Mock user object with email for Celery task
        mock_user = MagicMock()
        mock_user.email = "test@test.com"
        mock_user_repo_instance.get_by_id.return_value = mock_user

        if is_valid:
            # Expect success
            result = await service.create_booking(user_id=1, table_id=1, start_time=booking_time)
            assert result == fake_booking
        else:
            # Expect ValueError based on business rules
            with pytest.raises(ValueError):
                await service.create_booking(user_id=1, table_id=1, start_time=booking_time)
