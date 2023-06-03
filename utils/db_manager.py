from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings

settings = get_settings()


class MongoDBManager:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.mongo_db_url)
        self.database = self.client.get_database(settings.mongo_db_name)

    def get_collection(self, collection_name: str):
        return self.database.get_collection(collection_name)
