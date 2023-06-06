from typing import List
from fastapi import HTTPException

from pymongo import ReturnDocument
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe_models import RecipeBase, RecipeView, RecipeLike, RecipeCreate
from datetime import datetime
settings = get_settings()


class RecipeDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("recipes")

    # get

    async def get_all_recipes(self):
        cursor = self.collection.find({})
        result = await cursor.to_list(length=None)
        return result

    async def get_recipes_by_categories(self, category):
        result = await self.collection.find({"recipe_category": category}).to_list(length=None)
        return result

    async def get_recipes_by_popularity(self):
        results = await self.collection.find({"recipe_like": {"$gte": 1}}).to_list(length=None)
        return results

    async def get_recipe_by_recipe_id(self, id):
        result = await self.collection.find_one({"recipe_id": id})
        if result is None:
            return None
        return RecipeCreate(**result)

    async def get_recipes_by_user_id(self, user_id):
        result = await self.collection.find({"user_id": user_id}).to_list(length=None)
        return result

     # post

    async def register_recipe(self, recipe: RecipeCreate):
        recipe_data = recipe.dict()
        #  생성일자를 추가합니다.
        recipe_data["created_at"] = datetime.utcnow()
        await self.collection.insert_one(recipe.dict())
        return {"recipe_id": recipe.recipe_id, "full": recipe}

    async def register_recipes(self, recipes: List[RecipeCreate]):
        recipe_data = [recipe.dict() for recipe in recipes]
        result = await self.collection.insert_many(recipe_data)
        if len(result.inserted_ids) != len(recipe_data):
            raise HTTPException(
                status_code=500,
                detail="Error occurred while inserting recipes"
            )
        return {"message": "Recipes inserted successfully"}

     # update

    async def update_recipe(self, recipe_id: str, updated_recipe: RecipeBase):
        updated_recipe_dict = updated_recipe.dict(exclude={"recipe_id"})
        updated_document = await self.collection.find_one_and_update(
            {"recipe_id": recipe_id},
            {"$set": updated_recipe_dict},
            return_document=ReturnDocument.AFTER
        )
        if updated_document is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        return updated_document

    async def update_recipe_view(self, recipe_id: str):
        update_query = {"$inc": {"recipe_view": 1}}
        result = await self.collection.update_one({"recipe_id": recipe_id}, update_query)
        return result.modified_count

    async def update_recipe_like(self, recipe_id: str):
        update_query = {"$inc": {"recipe_like": 1}}
        result = await self.collection.update_one({"recipe_id": recipe_id}, update_query)
        if result.modified_count > 0:
            updated_recipe = await self.collection.find_one({"recipe_id": recipe_id})
            return updated_recipe
        else:
            return None

     # delete

    async def delete_one_recipe(self, recipe_id: str):
        result = await self.collection.delete_one({"recipe_id": recipe_id})
        if result.deleted_count == 1:
            return 1  # 문서가 성공적으로 삭제되었을 경우
        else:
            return 0  # 문서 삭제 실패

    async def delete_all_recipe(self):
        result = await self.collection.delete_many({})
        if result.deleted_count != 0:
            return 1  # 문서가 성공적으로 삭제되었을 경우
        else:
            return 0  # 문서 삭제 실패

    #    페이지 네이션
    #     return result
    # async def get_all_recipes(self, offset=0, limit=16):
    #     result = await self.collection.find().skip(offset).limit(limit).to_list(length=None)
    #     return result
