import secrets
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.users.models import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from .schemas import LoginRequest, RegisterRequest


async def login(payload: LoginRequest, db: AsyncSession) -> dict:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta desativada")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    user.refresh_token = refresh_token
    await db.commit()

    return {"accessToken": access_token, "refreshToken": refresh_token, "user": user}


async def register(payload: RegisterRequest, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado")

    user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        verify_token=secrets.token_urlsafe(32),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def logout(user: User, db: AsyncSession) -> None:
    user.refresh_token = None
    await db.commit()


async def refresh(refresh_token: str, db: AsyncSession) -> dict:
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    result = await db.execute(select(User).where(User.id == payload["sub"]))
    user = result.scalar_one_or_none()

    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")

    access_token = create_access_token({"sub": user.id})
    return {"accessToken": access_token}


async def forgot_password(email: str, db: AsyncSession) -> None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        user.reset_token = secrets.token_urlsafe(32)
        await db.commit()
        # TODO: enviar email com o token


async def reset_password(token: str, new_password: str, db: AsyncSession) -> None:
    result = await db.execute(select(User).where(User.reset_token == token))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")

    user.password = hash_password(new_password)
    user.reset_token = None
    await db.commit()


async def verify_email(code: str, db: AsyncSession) -> None:
    result = await db.execute(select(User).where(User.verify_token == code))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código inválido")

    user.is_verified = True
    user.verify_token = None
    await db.commit()
