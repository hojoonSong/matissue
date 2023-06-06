from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.user_models import UserInDB
from fastapi import HTTPException

settings = get_settings()


class UserDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("users")

    async def create_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.insert_one(user_in_db.dict())
        return str(result.inserted_id)

    async def update_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.replace_one({"user_id": user_in_db.user_id}, user_in_db.dict())
        return result.modified_count == 1

    async def delete_user(self, user_id: str):
        delete_result = await self.collection.delete_one({"user_id": user_id})
        return delete_result.deleted_count > 0

    async def get_user_by_id(self, user_id: str):
        user_doc = await self.collection.find_one({"user_id": user_id})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_user_by_email(self, email: str):
        user_doc = await self.collection.find_one({"email": email})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_users(self):
        user_docs = self.collection.find({})
        users = []
        async for user_doc in user_docs:
            users.append(UserInDB(**user_doc))
        return users

    async def modify_subscription(self, current_user: str, follow_user_id: str, subscribe: bool) -> None:
        user = await self.get_user_by_id(current_user)
        follow_user = await self.get_user_by_id(follow_user_id)

        if not user or not follow_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        if subscribe:
            if follow_user_id in user.follows:
                raise HTTPException(status_code=409, detail="이미 구독 중입니다")
            else:
                user.follows.append(follow_user_id)

        else:
            if follow_user_id in user.follows:
                user.follows.remove(follow_user_id)
            else:
                raise HTTPException(status_code=409, detail="구독을 취소할 수 없습니다.")

        await self.update_user_in_db(user)

    async def get_followers(self, user_id: str):
        follower_docs = self.collection.find({"follows": user_id})
        followers = []
        async for follower_doc in follower_docs:
            followers.append(UserInDB(**follower_doc))
        return followers


def get_user_dao() -> UserDao:
    db_manager = MongoDBManager()
    return UserDao(db_manager)
