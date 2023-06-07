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

    async def get_comments(self, recipe_id):
        result = await self.recipe_dao.get_comments(recipe_id)
        return result

    async def get_one_comment(self, comment_id):
        result = await self.recipe_dao.get_one_comment(comment_id)
        return result

     # post

    async def register_recipe(self, recipe: RecipeCreate):
        result = await self.recipe_dao.register_recipe(recipe)
        return result

    async def register_recipes(self, recipes: List[RecipeCreate]):
        result = await self.recipe_dao.register_recipes(recipes)
        return result

    async def register_comment(self, recipe_id, comment):
        result = await self.recipe_dao.register_comment(recipe_id, comment)
        return result
     # update

    async def update_recipe(self, recipe_id, updated_recipe, current_user):
        result = await self.recipe_dao.update_recipe(recipe_id, updated_recipe, current_user)
        return result

    async def update_recipe_view(self, recipe_id: str):
        result = await self.recipe_dao.update_recipe_view(recipe_id)
        return result

    async def update_recipe_like(self, recipe_id: str):
        result = await self.recipe_dao.update_recipe_like(recipe_id)
        return result

    async def update_comment(self, comment_id, comment, current_user):
        result = await self.recipe_dao.update_comment(comment_id, comment, current_user)
        return result

     # delete

    async def delete_one_recipe(self, recipe_id: str, current_user):
        result = await self.recipe_dao.delete_one_recipe(recipe_id, current_user)
        return result

    async def delete_all_recipe(self):
        result = await self.recipe_dao.delete_all_recipe()
        return result

    async def delete_comment(self, comment_id, current_user):
        result = await self.recipe_dao.delete_comment(comment_id, current_user)
        return result
