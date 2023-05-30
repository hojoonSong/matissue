from models.user import UserIn, UserInDB
from utils.hashing import Hasher
from utils.session_manager import SessionManager
from datetime import datetime
from dao.user_dao import UserDao
from fastapi import HTTPException
from utils.config import get_settings
import redis

settings = get_settings()

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)


MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT = 3600


class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao
        self.session_manager = SessionManager()

    async def create_user(self, user: UserIn):
        existing_user = await self.user_dao.get_user_by_id(user.user_id)
        if existing_user:
            raise HTTPException(
                status_code=404, detail=f"사용자 아이디 '{user.user_id}'은 사용할 수 없습니다.")

        exiting_email = await self.user_dao.get_user_by_email(user.email)
        if exiting_email:
            raise HTTPException(
                status_code=404, detail=f"사용자 이메일 '{user.email}'은 사용할 수 없습니다.")

        user_in_db = UserInDB(
            **user.dict(exclude={'password'}),
            hashed_password=Hasher.get_hashed_password(user.password),
            created_at=datetime.now()
        )
        return await self.user_dao.create_user_in_db(user_in_db)

    async def login(self, user_id: str, password: str):
        timeout_key = f'timeout:{user_id}'
        remaining_time = r.ttl(timeout_key)
        if remaining_time > 0:
            raise HTTPException(
                status_code=429, detail=f"로그인 시도가 초과되었습니다. {remaining_time}초 후에 다시 시도해주세요.")

        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not Hasher.verify_password(password, user.hashed_password):
            failed_key = f'failed:{user_id}'
            failed_attempts = r.incr(failed_key)
            if failed_attempts >= MAX_LOGIN_ATTEMPTS:
                r.set(timeout_key, '1', LOGIN_TIMEOUT)
                r.delete(failed_key)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = self.session_manager.create_session(user.user_id)
        return {"session_id": session_id}

    async def logout(self, session_id: str):
        self.session_manager.delete_session(session_id)
        return {"detail": "성공적으로 로그아웃되었습니다."}
