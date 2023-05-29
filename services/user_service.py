from models.user import UserIn, UserInDB
from utils.hashing import Hasher
from utils.session_manager import SessionManager
from datetime import datetime
from dao.user_dao import UserDao
from fastapi import HTTPException


class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao
        self.session_manager = SessionManager()

    async def create_user(self, user: UserIn):
        user_in_db = UserInDB(
            **user.dict(exclude={'password'}),
            hashed_password=Hasher.get_hashed_password(user.password),
            created_at=datetime.now()
        )
        return await self.user_dao.create_user_in_db(user_in_db)

    async def login(self, user_id: str, password: str):
        user = await self.user_dao.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not Hasher.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        session_id = self.session_manager.create_session(user.user_id)
        return {"session_id": session_id}
