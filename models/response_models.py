from pydantic import BaseModel
from typing import List, Optional


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


class ErrorResponse(BaseModel):
    detail: str


class Customer(BaseModel):
    user_id: str
    username: str
    img: str


class PeopleResponse(BaseModel):
    people: List[Customer]
