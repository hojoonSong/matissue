from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.user import UserInDB

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
        if result.modified_count == 1:
            return True
        else:
            return False

    async def delete_user(self, user_id: str):
        delete_result = await self.collection.delete_one({"user_id": user_id})
        if delete_result.deleted_count:
            return True
        return False

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


class UserDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("users")

    async def create_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.insert_one(user_in_db.dict())
        return str(result.inserted_id)

    async def update_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.replace_one({"user_id": user_in_db.user_id}, user_in_db.dict())
        if result.modified_count == 1:
            return True
        else:
            return False

    async def delete_user(self, user_id: str):
        delete_result = await self.collection.delete_one({"user_id": user_id})
        if delete_result.deleted_count:
            return True
        return False

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
