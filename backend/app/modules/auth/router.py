from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.users.models import User
from . import service
from .schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await service.login(body, db)


@router.post("/register", status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    await service.register(body, db)


@router.post("/logout", status_code=204)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await service.logout(current_user, db)


@router.post("/refresh")
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await service.refresh(body.refreshToken, db)


@router.post("/forgot-password", status_code=204)
async def forgot_password(body: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    await service.forgot_password(body.email, db)


@router.post("/reset-password", status_code=204)
async def reset_password(body: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    await service.reset_password(body.token, body.newPassword, db)


@router.post("/verify-email", status_code=204)
async def verify_email(body: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    await service.verify_email(body.code, db)
