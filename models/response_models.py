from pydantic import BaseModel


class LoginResponse(BaseModel):
    message: str
    session_id: str


class LoginRequest(BaseModel):
    user_id: str
    password: str


class DeleteRequest(LoginRequest):
    session_id: str


class LogoutRequest(BaseModel):
    session_id: str


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
