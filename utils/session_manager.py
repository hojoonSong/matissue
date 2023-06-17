from fastapi import Depends, HTTPException, status, Header, Request
from pydantic import BaseModel
from models.user_models import UserInDB, UserIn
from typing import Optional
from .config import get_settings
from .hash_manager import Hasher
import uuid
import random
import string
import redis
from datetime import datetime


settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


class Session(BaseModel):
    id: Optional[str] = Header(None)


class SessionManager:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            settings.redis_url, decode_responses=True
        )

    def create_session(self, data: str):
        session_id = str(uuid.uuid4())
        self.redis_client.set(session_id, data)
        return session_id

    def get_session(self, session_id: str, expiration: int = 3600):
        if session_id is None:
            raise ValueError("Session ID cannot be None")
        data = self.redis_client.get(session_id)
        if data is None:
            raise HTTPException(status_code=401, detail="Invalid session id")
        self.redis_client.expire(session_id, expiration)
        return data

    async def delete_session(self, session_id: str):
        result = self.redis_client.delete(session_id)
        return result > 0

    def create_verification_code(self, email: str):
        verification_code = str(uuid.uuid4())
        self.redis_client.set(verification_code, email, ex=86400)
        return verification_code

    def verify_email(self, code: str):
        email = self.redis_client.get(code)
        if email is None:
            return False
        self.redis_client.delete(code)
        return email

    async def save_user_info(self, user: UserIn):
        hashed_password = await Hasher.get_hashed_password(user.password)
        user_in_redis = UserInDB(
            **user.dict(exclude={"password"}),
            hashed_password=hashed_password,
            created_at=datetime.now(),
        )
        user_json = user_in_redis.json()
        self.redis_client.set(user_in_redis.email, user_json, ex=86400)

    def get_user_info(self, email: str):
        user_json = self.redis_client.get(email)
        if user_json is None:
            return None
        user_in_redis = UserInDB.parse_raw(user_json)
        return UserInDB(**user_in_redis.dict(), password=user_in_redis.hashed_password)

    def create_email_verification_code(self, email: str):
        verification_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        self.redis_client.set(verification_code, email, ex=1800)
        return verification_code

    def check_verification_code(self, email: str, code: str):
        verified_email = self.verify_email(code)
        return verified_email == email


def get_verification_link(email: str, verification_code: str) -> str:
    base_url = "https://www.matissue.com/auth/verify"
    verification_link = f"{base_url}?code={verification_code}"
    return verification_link


def get_current_session(request: Request) -> str:
    session_id = request.cookies.get("session-id")
    session_manager = SessionManager()
    current_user = session_manager.get_session(session_id)
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )
    return current_user


async def get_current_user(
    session: Session = Depends(),
    session_manager: SessionManager = Depends(SessionManager),
):
    if session.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesssion ID가 없습니다."
        )
    user_id = session_manager.get_session(session.id)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session ID",
        )
    return user_id


async def verify_email(
    code: str, session_manager: SessionManager = Depends(SessionManager)
):
    verification_result = session_manager.verify_email(code)
    if not verification_result:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"message": "Email verification successful"}
