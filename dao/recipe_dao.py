from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe import RecipeBase

settings = get_settings()


class RecipeDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("recipes")

    async def get_all_recipe(self):
        result = await self.collection.find().to_list(length=None)
        return result

    async def post_one_recipe(self, new_recipe: RecipeBase):
        result = await self.collection.insert_one(new_recipe)
        # print("dao", new_recipe)
        # print("dao", result.inserted_id)
        new = await self.collection.find_one({"_id": result.inserted_id})
        # print("dao", new)
        return new

    async def get_recipe_by_id(self, recipe_id: str):
        # 데이터베이스에서 레시피 정보 조회
        result = await self.collection.find_one({"recipe_id": recipe_id})
        return result

        # ...
    async def update_recipe_view(self, recipe_id: str):
        # 레시피 정보를 데이터베이스에 저장
        update_query = {"$inc": {"recipe_view": 1}}
        result = await self.collection.update_one({"recipe_id": recipe_id}, update_query)
        return result.modified_count

    async def update_recipe_like(self, recipe_id: str):
        # 레시피 정보를 데이터베이스에 저장
        update_query = {"$inc": {"recipe_like": 1}}
        result = await self.collection.update_one({"recipe_id": recipe_id}, update_query)
        return result.modified_count

    async def delete_one_recipe(self, recipe_id: str):
        result = await self.collection.delete_one({"recipe_id": recipe_id})
        if result.acknowledged:
            return 1  # 문서가 성공적으로 삭제되었을 경우
        else:
            return 0  # 문서 삭제
