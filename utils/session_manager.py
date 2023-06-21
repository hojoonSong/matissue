from fastapi import Depends, HTTPException, status, Header, Request
from pydantic import BaseModel
from models.user_models import UserInDB, UserIn
from typing import Optional
from .config import get_settings
from .hash_manager import Hasher
import uuid
import random
import string
import aioredis
import datetime
from datetime import datetime, timedelta


settings = get_settings()


class Session(BaseModel):
    id: Optional[str] = Header(None)


class SessionManager:
    def __init__(self):
        self.redis_client = None

    async def get_redis_client(self):
        if self.redis_client is None:
            self.redis_client = await aioredis.from_url(
                settings.redis_url, encoding="utf-8", decode_responses=True
            )
        return self.redis_client

    async def create_session(self, data: str):
        session_id = str(uuid.uuid4())
        redis_client = await self.get_redis_client()
        await redis_client.set(session_id, data)
        return session_id

    async def get_session(self, session_id: str, expiration: int = 3600):
        if session_id is None:
            raise ValueError("Session ID cannot be None")

        redis_client = await self.get_redis_client()

        # Use a pipeline to group the commands
        pipeline = redis_client.pipeline()
        pipeline.get(session_id)
        pipeline.expire(session_id, expiration)

        # Execute the commands in a single request
        data, _ = await pipeline.execute()

        if data is None:
            raise HTTPException(status_code=401, detail="Invalid session id")

        return data

    async def delete_session(self, session_id: str):
        redis_client = await self.get_redis_client()
        result = await redis_client.delete(session_id)
        return result > 0

    async def create_verification_code(self, email: str):
        verification_code = str(uuid.uuid4())
        redis_client = await self.get_redis_client()
        await redis_client.set(verification_code, email)
        await redis_client.expire(verification_code, 86400)
        return verification_code

    async def verify_email(self, code: str):
        redis_client = await self.get_redis_client()
        email = await redis_client.get(code)
        if email is None:
            return False
        await redis_client.delete(code)
        return email

    async def save_user_info(self, user: UserIn):
        hashed_password = await Hasher.get_hashed_password(user.password)
        user_in_redis = UserInDB(
            **user.dict(exclude={"password"}),
            hashed_password=hashed_password,
            created_at=datetime.now(),
        )
        user_json = user_in_redis.json()
        redis_client = await self.get_redis_client()
        await redis_client.set(user_in_redis.email, user_json)
        await redis_client.expire(user_in_redis.email, 86400)

    async def get_user_info(self, email: str):
        redis_client = await self.get_redis_client()
        user_json = await redis_client.get(email)
        if user_json is None:
            return None
        user_in_redis = UserInDB.parse_raw(user_json)
        return UserInDB(**user_in_redis.dict(), password=user_in_redis.hashed_password)

    async def create_email_verification_code(self, email: str):
        verification_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        redis_client = await self.get_redis_client()
        await redis_client.set(verification_code, email, expire=1800)
        return verification_code

    async def check_verification_code(self, email: str, code: str):
        verified_email = await self.verify_email(code)
        return verified_email == email


def get_verification_link(email: str, verification_code: str) -> str:
    base_url = "https://www.matissue.com/auth/verify"
    verification_link = f"{base_url}?code={verification_code}"
    return verification_link


async def get_current_session(request: Request) -> str:
    session_id = request.cookies.get("session-id")
    session_manager = SessionManager()
    current_user = await session_manager.get_session(session_id)

    # 관리자인 경우, 예외처리를 합니다.
    if current_user and getattr(current_user, "id", None) == "admin":
        return current_user

    # 일반적인 처리로 변경.
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid session ID",
        )

    return current_user


async def verify_email(
    code: str, session_manager: SessionManager = Depends(SessionManager)
):
    verification_result = await session_manager.verify_email(code)
    if not verification_result:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"message": "Email verification successful"}
