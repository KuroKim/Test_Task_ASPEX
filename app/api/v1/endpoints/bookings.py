import uuid
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.booking import BookingCreate, BookingRead
from app.schemas.table import TableRead
from app.services.booking_service import BookingService
from app.models.user import User

router = APIRouter()


@router.get("/tables/available", response_model=List[TableRead])
async def get_available_tables(
        datetime_query: datetime,
        db: AsyncSession = Depends(deps.get_db)
):
    """
    Retrieve list of available tables for a specific date and time.
    Example: 2026-02-10T18:00:00
    """
    service = BookingService(db)
    return await service.get_available_tables_for_time(datetime_query)


@router.post("/", response_model=BookingRead)
async def create_booking(
        booking_in: BookingCreate,
        current_user: User = Depends(deps.get_current_user),
        db: AsyncSession = Depends(deps.get_db)
):
    """
    Create a new table reservation for the authenticated user.
    """
    service = BookingService(db)
    try:
        return await service.create_booking(
            user_id=current_user.id,
            table_id=booking_in.table_id,
            start_time=booking_in.booking_start
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my", response_model=List[BookingRead])
async def get_my_bookings(
        current_user: User = Depends(deps.get_current_user),
        db: AsyncSession = Depends(deps.get_db)
):
    """
    Get all active and future bookings for the authenticated user.
    """
    service = BookingService(db)
    return await service.get_user_bookings(current_user.id)


@router.delete("/{booking_id}", status_code=204)
async def cancel_booking(
        booking_id: uuid.UUID,
        current_user: User = Depends(deps.get_current_user),
        db: AsyncSession = Depends(deps.get_db)
):
    """
    Cancel an existing booking (at least 1 hour prior to start time).
    """
    service = BookingService(db)
    try:
        await service.delete_booking(booking_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
