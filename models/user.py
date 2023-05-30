from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime, date
from fastapi import HTTPException
import re


class UserBase(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    birth_date: Optional[date]
    img: Optional[str]


class UserIn(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, password):
        if len(password) < 8 or not re.findall("\d", password) or not re.findall("[A-Z]", password) or not re.findall("[a-z]", password):
            raise HTTPException(
                status_code=400, detail='비밀번호는 8글자 이상, 숫자와 문자를 혼용하여야 합니다.')
        return password

    @validator('user_id')
    def validate_user_id(cls, user_id):
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            raise HTTPException(
                status_code=400, detail='사용자 아이디는 영문자, 숫자, 밑줄(_), 대시(-)만 포함할 수 있습니다.')
        return user_id


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


class LogoutRequest(BaseModel):
    session_id: str


class MessageResponse(BaseModel):
    message: str
