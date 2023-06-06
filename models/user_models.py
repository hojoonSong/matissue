from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
import re


class UserBase(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    birth_date: Optional[str]
    img: str


class UserIn(UserBase):
    password: str

    @validator('birth_date', pre=True)
    def parse_birth_date(cls, value: str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise HTTPException(
                status_code=400, detail='birth_date는 "YYYY-MM-DD" 형식이어야 합니다.')

    @validator('password')
    def validate_password(cls, password):
        if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password) or not re.search(r"[^\w\s]", password):
            raise HTTPException(
                status_code=400, detail='비밀번호는 8글자 이상, 대소문자, 특수문자, 숫자를 혼용하여야 합니다.')
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


class UserUpdate(UserBase):
    username: Optional[str]
    email: Optional[EmailStr]
    birth_date: Optional[str]
    img: Optional[str]
    password: Optional[str]

    @validator('birth_date', pre=True)
    def parse_birth_date(cls, value: str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise HTTPException(
                status_code=400, detail='birth_date는 "YYYY-MM-DD" 형식이어야 합니다.')

    @validator('password')
    def validate_password(cls, password: str):
        if len(password) < 8 or not re.search("\d", password) or not re.search("[A-Z]", password) or not re.search("[a-z]", password):
            raise HTTPException(
                status_code=400, detail='비밀번호는 8글자 이상, 숫자와 대소문자를 혼용하여야 합니다.')
        return password
