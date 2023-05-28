from motor.motor_asyncio import AsyncIOMotorClient
from models.user import UserInDB
from utils.config import get_settings

settings = get_settings()


class UserDao:
    def __init__(self, db: AsyncIOMotorClient = None):
        self.db = db or AsyncIOMotorClient(settings.mongo_db_url)
        self.collection = self.db.get_database(
            settings.mongo_db_name).get_collection("users")

    async def create_user_in_db(self, user_in_db: UserInDB):
        result = await self.collection.insert_one(user_in_db.dict())
        return str(result.inserted_id)
