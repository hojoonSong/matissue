from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe import Recipe

settings = get_settings()


class RecipeDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("recipes")

    async def get_all_recipe(self):
        result = await self.collection.find().to_list(length=None)
        return result

    async def post_one_recipe(self, new_recipe: Recipe):
        result = await self.collection.insert_one(new_recipe)
        return result
