from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime, date


class UserBase(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    birth_date: Optional[date]


class UserIn(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        return password


class UserOut(UserBase):
    created_at: Optional[datetime] = Field(...)


class UserInDB(UserBase):
    hashed_password: str
    created_at: Optional[datetime]


class LoginResponse(BaseModel):
    message: str
    session_id: str


class LoginRequest(BaseModel):
    user_id: str
    password: str
