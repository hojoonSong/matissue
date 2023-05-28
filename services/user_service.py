from models.user import UserIn, UserInDB
from utils.hashing import Hasher
from dao.user_dao import UserDao


class UserService:
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    async def create_user(self, user: UserIn):
        user_in_db = UserInDB(
            **user.dict(), hashed_password=Hasher.get_hashed_password(user.password)
        )
        return await self.user_dao.create_user_in_db(user_in_db)
