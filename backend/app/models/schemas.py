from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProfileUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    age: int | None = Field(default=None, ge=13, le=120)
    height: float | None = Field(default=None, ge=50, le=250)
    weight: float | None = Field(default=None, ge=20, le=400)
    activity_level: str | None = None
    dietary_preference: str | None = None
    goal: str | None = None
    allergies: str | None = Field(default=None, max_length=500)


class ProfileResponse(ProfileUpdate):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PlanResponse(BaseModel):
    id: int
    breakfast: str
    lunch: str
    snack: str
    dinner: str
    nutrition_summary: str
    hydration_reminder: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class FileResponse(BaseModel):
    id: int
    filename: str
    storage_path: str
    content_type: str | None
    size_bytes: int
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)
