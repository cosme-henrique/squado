from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar: str | None
    role: str

    model_config = {"from_attributes": True}


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    avatar: str | None = None
