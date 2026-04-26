from pydantic import BaseModel, EmailStr
from app.modules.users.schemas import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refreshToken: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str


class VerifyEmailRequest(BaseModel):
    code: str


class LoginResponse(BaseModel):
    accessToken: str
    refreshToken: str
    user: UserResponse
