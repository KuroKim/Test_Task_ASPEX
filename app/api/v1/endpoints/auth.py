from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService
from app.core.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(
        user_in: UserCreate,
        db: AsyncSession = Depends(deps.get_db)
):
    service = AuthService(db)
    try:
        return await service.register_new_user(user_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(deps.get_db)
):
    service = AuthService(db)
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
