from models.user_models import UserIn, UserInDB, UserUpdate
from utils.hash_manager import Hasher
from utils.session_manager import SessionManager
from dao.user_dao import UserDao, get_user_dao
from fastapi import HTTPException, Response, Depends
from utils.config import get_settings
from utils.permission_manager import check_user_permissions
import secrets
import secrets
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

    async def create_user(cls, user: UserIn):
        await cls.validate_user_creation(user)
        user_in_db = UserInDB(
            **user.dict(exclude={"password"}),
        )
        return await cls.user_dao.create_user_in_db(user_in_db)

    async def delete_user(
        self, user_id: str, password: str, session_id: str, current_user: str
    ):
        check_user_permissions(user_id, current_user)
        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"사용자 아이디가 존재하지 않습니다.")

        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail=f"비밀번호가 일치하지 않습니다.")

        self.session_manager.delete_session(session_id)
        return await self.user_dao.delete_user(user_id)

    async def update_user(self, user: UserUpdate, current_user):
        check_user_permissions(user.user_id, current_user)
        current_user_in_db = await self.user_dao.get_user_by_id(user.user_id)

        if not current_user_in_db:
            raise Exception(f"사용자 아이디 '{user.user_id}'을(를) 찾을 수 없습니다.")

        if (
            current_user != "admin"
            and user.email is not None
            and user.email != current_user_in_db.email
        ):
            if not self.session_manager.check_verification_code(
                user.email, user.email_code
            ):
                raise Exception("잘못된 인증 코드입니다.")

        existing_email_user = await self.user_dao.get_user_by_email(user.email)
        if existing_email_user and existing_email_user.user_id != user.user_id:
            raise Exception(f"사용자 이메일 '{user.email}'은(는) 사용할 수 없습니다.")

        update_data = user.dict(exclude_unset=True, exclude={"password"})
        if user.password:
            hashed_password = await Hasher.get_hashed_password(user.password)
            update_data["hashed_password"] = hashed_password

        await self.user_dao.update_user_in_db(user.user_id, update_data)
        updated_user = await self.user_dao.get_user_by_id(user.user_id)
        return updated_user

    async def login(self, user_id: str, password: str):
        timeout_key = f"timeout:{user_id}"
        remaining_time = redis_client.ttl(timeout_key)
        if remaining_time > 0:
            raise HTTPException(
                status_code=429,
                detail=f"로그인 시도가 초과되었습니다. {remaining_time}초 후에 다시 시도해주세요.",
            )

        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not Hasher.verify_password(password, user.hashed_password):
            failed_key = f"failed:{user_id}"
            failed_attempts = redis_client.incr(failed_key)
            if failed_attempts >= MAX_LOGIN_ATTEMPTS:
                redis_client.set(timeout_key, "1", LOGIN_TIMEOUT)
                redis_client.delete(failed_key)
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = self.session_manager.create_session(user.user_id)
        return {"session_id": session_id}

    async def logout(self, session_id: str, response: Response):
        if session_id is None:
            raise HTTPException(status_code=400, detail="세션 ID를 찾을 수 없습니다.")

        response.delete_cookie(key="session_id")
        session = await self.session_manager.delete_session(session_id)

        if not session:
            return {"detail": "세션 ID가 없거나 이미 로그아웃되었습니다."}

        return {"detail": "성공적으로 로그아웃되었습니다."}

    async def create_temporary_password(self, user_id: str):
        temporary_password = secrets.token_hex(8)
        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"'{user_id}'를 찾을 수 없습니다.")

        hashed_temporary_password = await Hasher.get_hashed_password(temporary_password)
        update_data = {"hashed_password": hashed_temporary_password}
        if await self.user_dao.update_user_in_db(user_id, update_data):
            return temporary_password
        else:
            return None

    async def validate_user_creation(self, user: UserIn):
        existing_user = await self.user_dao.get_user_by_id(user.user_id)
        if existing_user:
            raise HTTPException(
                status_code=404, detail=f"사용자 아이디 '{user.user_id}'은 사용할 수 없습니다."
            )

        existing_email = await self.user_dao.get_user_by_email(user.email)
        if existing_email:
            raise HTTPException(
                status_code=404, detail=f"사용자 이메일 '{user.email}'은 사용할 수 없습니다."
            )

    async def modify_subscribe_user(
        self, current_user: str, follow_user_id: str, subscribe: bool
    ) -> None:
        await self.user_dao.modify_subscription(current_user, follow_user_id, subscribe)

    async def get_fans(self, user_id: str):
        return await self.user_dao.get_fans(user_id)

    async def get_subscriptions(self, user_id: str):
        return await self.user_dao.get_subscriptions(user_id)

    async def is_user_subscribed(self, current_user: str, follow_user_id: str) -> bool:
        return await self.user_dao.is_user_subscribed(current_user, follow_user_id)


def get_user_service(user_dao: UserDao = Depends(get_user_dao)) -> UserService:
    return UserService(user_dao)
