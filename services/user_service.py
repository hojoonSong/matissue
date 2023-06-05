from models.user_models import UserIn, UserInDB
from utils.hash_manager import Hasher
from utils.session_manager import SessionManager
from datetime import datetime
from dao.user_dao import UserDao
from fastapi import HTTPException, Response
from utils.config import get_settings
from utils.permission_manager import check_user_permissions
import redis

settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)


MAX_LOGIN_ATTEMPTS = 5
LOGIN_TIMEOUT = 3600


class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao
        self.session_manager = SessionManager()
        self.response = Response()

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

    async def delete_user(self, user_id: str, password: str, session_id: str):
        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"사용자 아이디가 존재하지 않습니다.")

        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail=f"비밀번호가 일치하지 않습니다.")

        self.session_manager.delete_session(session_id)
        return await self.user_dao.delete_user(user_id)

    async def update_user(self, user: UserInDB):
        check_user_permissions(user.user_id)
        existing_user = await self.user_dao.get_user_by_id(user.user_id)
        if not existing_user:
            raise HTTPException(
                status_code=404, detail=f"사용자 아이디 '{user.user_id}'은 찾을 수 없습니다.")

        existing_email_user = await self.user_dao.get_user_by_email(user.email)
        if existing_email_user and existing_email_user.user_id != user.user_id:
            raise HTTPException(
                status_code=400, detail=f"사용자 이메일 '{user.email}'은 사용할 수 없습니다.")

        user_in_db = UserInDB(
            **user.dict(exclude={'password'}),
            hashed_password=Hasher.get_hashed_password(
                user.password) if user.password else existing_user.hashed_password,
            created_at=datetime.now())

        await self.user_dao.update_user_in_db(user_in_db)
        return True

    async def login(self, user_id: str, password: str):
        timeout_key = f'timeout:{user_id}'
        remaining_time = redis_client.ttl(timeout_key)
        if remaining_time > 0:
            raise HTTPException(
                status_code=429, detail=f"로그인 시도가 초과되었습니다. {remaining_time}초 후에 다시 시도해주세요.")

        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not Hasher.verify_password(password, user.hashed_password):
            failed_key = f'failed:{user_id}'
            failed_attempts = redis_client.incr(failed_key)
            if failed_attempts >= MAX_LOGIN_ATTEMPTS:
                redis_client.set(timeout_key, '1', LOGIN_TIMEOUT)
                redis_client.delete(failed_key)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = self.session_manager.create_session(user.user_id)
        return {"session_id": session_id}

    async def logout(self, session_id: str, response: Response):
        response.delete_cookie(key="session_id")
        session = await SessionManager.delete_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"detail": "성공적으로 로그아웃되었습니다."}
