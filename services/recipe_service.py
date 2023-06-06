from typing import List
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe_models import RecipeBase, RecipeView, RecipeLike, RecipeCreate
from dao.recipe_dao import RecipeDao


settings = get_settings()
db_manager = MongoDBManager()
collection = db_manager.get_collection("recipes")

recipe_dao = RecipeDao()


class RecipeService:
    def __init__(self, recipe_dao: RecipeDao):
        self.recipe_dao = recipe_dao

    async def get_all_recipes(self):
        result = await self.recipe_dao.get_all_recipes()
        return result

    async def get_recipes_by_categories(self, category):
        result = await self.recipe_dao.get_recipes_by_categories(category)
        return result

    async def get_recipes_by_popularity(self):
        results = await self.recipe_dao.get_recipes_by_popularity()
        return results

    async def get_recipe_by_recipe_id(self, recipe_id):
        result = await self.recipe_dao.get_recipe_by_recipe_id(recipe_id)
        return result

    async def get_recipes_by_user_id(self, user_id):
        result = await self.recipe_dao.get_recipes_by_user_id(user_id)
        return result

    async def get_recipe_to_update_recipe(self, recipe_id):
        result = await self.recipe_dao.get_recipe_to_update_recipe(recipe_id)
        return result
     # post

    async def register_recipe(self, recipe: RecipeCreate):
        result = await self.recipe_dao.register_recipe(recipe)
        print('serviceresult: ', result)
        return result

    async def register_recipes(self, recipes: List[RecipeCreate]):
        result = await self.recipe_dao.register_recipes(recipes)
        print('serviceresult: ', result)
        return result

     # update

    async def update_recipe(self, recipe_id: str, updated_recipe: RecipeBase):
        result = await self.recipe_dao.update_recipe(recipe_id, updated_recipe)
        print('serviceresult: ', result)
        return result

    async def update_recipe_view(self, recipe_id: str):
        result = await self.recipe_dao.update_recipe_view(recipe_id)
        print('serviceresult: ', result)
        return result

    async def update_recipe_like(self, recipe_id: str):
        result = await self.recipe_dao.update_recipe_like(recipe_id)
        print('serviceresult: ', result)
        return result

     # delete

    async def delete_one_recipe(self, recipe_id: str):
        result = await self.recipe_dao.delete_one_recipe(recipe_id)
        print('serviceresult: ', result)
        return result

    async def delete_all_recipe(self):
        result = await self.recipe_dao.delete_all_recipe()
        print('serviceresult: ', result)
        return result
