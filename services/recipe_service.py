from typing import List

from fastapi import HTTPException
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe_models import RecipeBase, RecipeView, RecipeLike, RecipeCreate
from dao.recipe_dao import RecipeDao
import logging

settings = get_settings()
db_manager = MongoDBManager()
collection = db_manager.get_collection("recipes")

recipe_dao = RecipeDao()
logger = logging.getLogger(__name__)


class RecipeService:
    def __init__(self, recipe_dao: RecipeDao):
        self.recipe_dao = recipe_dao

    async def get_all_recipes(self,skip: int = 0, limit: int = 160):
        try:
            result = await self.recipe_dao.get_all_recipes(skip=skip, limit=limit)
            return result
        except Exception as e:
            logger.error(f"Failed to get all recipes: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get all recipes"
            )

    async def get_recipes_by_categories(self, category, skip: int = 0, limit: int = 160):
        try:
            result = await self.recipe_dao.get_recipes_by_categories(category, skip=skip, limit=limit)
            return result
        except Exception as e:
            logger.error(f"Failed to get recipes by categories: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by categories"
            )

    async def get_recipes_by_popularity(self):
        try:
            results = await self.recipe_dao.get_recipes_by_popularity()
            return results
        except Exception as e:
            logger.error(f"Failed to get recipes by popularity: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by popularity"
            )

    async def get_recipes_by_latest(self, skip: int = 0, limit: int = 160):
        try:
            results = await self.recipe_dao.get_recipes_by_latest(skip=skip, limit=limit)
            return results
        except Exception as e:
            logger.error(f"Failed to get recipes by latest: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by latest"
            )

    async def get_recipes_by_single_serving(self):
        try:
            results = await self.recipe_dao.get_recipes_by_single_serving()
            return results
        except Exception as e:
            logger.error(f"Failed to get recipes by single serving: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by single serving"
            )

    async def get_recipes_by_vegetarian(self):
        try:
            results = await self.recipe_dao.get_recipes_by_vegetarian()
            return results
        except Exception as e:
            logger.error(f"Failed to get recipes by vegetarian: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by vegetarian"
            )

    async def get_recipes_by_ingredients(self, value):
        try:
            results = await self.recipe_dao.get_recipes_by_ingredients(value)
            return results
        except Exception as e:
            logger.error(f"Failed to get recipes by ingredients: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by ingredients"
            )

    async def get_recipe_by_recipe_id(self, recipe_id):
        try:
            result = await self.recipe_dao.get_recipe_by_recipe_id(recipe_id)
            return result
        except Exception as e:
            logger.error(f"Failed to get recipe by recipe id: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipe by recipe id"
            )

    async def get_recipes_by_user_id(self, user_id):
        try:
            result = await self.recipe_dao.get_recipes_by_user_id(user_id)
            return result
        except Exception as e:
            logger.error(f"Failed to get recipes by user id: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipes by user id"
            )

    async def get_recipe_to_update_recipe(self, recipe_id):
        try:
            result = await self.recipe_dao.get_recipe_to_update_recipe(recipe_id)
            return result
        except Exception as e:
            logger.error(f"Failed to get recipe to update recipe: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get recipe to update recipe"
            )

    async def get_comments(self, recipe_id):
        try:
            result = await self.recipe_dao.get_comments(recipe_id)
            return result
        except Exception as e:
            logger.error(f"Failed to get comments: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to get comments"
            )

    async def get_one_comment(self, comment_id):
        try:
            result = await self.recipe_dao.get_one_comment(comment_id)
            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="Comment not found"
                )
            return result
        except Exception as e:
            logger.error(f"댓글이 존재 하지 않습니다: {str(e)}")
            raise HTTPException(
                status_code=404,
                detail="댓글이 존재 하지 않습니다"
            )

     # post

    async def register_recipe(self, recipe: RecipeCreate):
        try:
            result = await self.recipe_dao.register_recipe(recipe)
            return result
        except Exception as e:
            logger.error(f"Failed to register recipe: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to register recipe"
            )

    async def register_recipes(self, recipes: List[RecipeCreate]):
        try:
            result = await self.recipe_dao.register_recipes(recipes)
            return result
        except Exception as e:
            logger.error(f"Failed to register recipes: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to register recipes"
            )

    async def register_comment(self, recipe_id, comment, current_user):
        try:
            result = await self.recipe_dao.register_comment(recipe_id, comment, current_user)
            return result
        except Exception as e:
            logger.error(f"Failed to register comment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to register comment"
            )
     # update

    async def update_recipe(self, recipe_id, updated_recipe, current_user):
        try:
            result = await self.recipe_dao.update_recipe(recipe_id, updated_recipe, current_user)
            return result
        except Exception as e:
            logger.error(f"Failed to update recipe: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update recipe"
            )

    async def update_recipe_view(self, recipe_id: str):
        try:
            result = await self.recipe_dao.update_recipe_view(recipe_id)
            return result
        except Exception as e:
            logger.error(f"Failed to update recipe view: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update recipe view"
            )

    async def update_recipe_like(self, recipe_id: str, current_user):
        try:
            result = await self.recipe_dao.update_recipe_like(recipe_id, current_user)
            return result
        except Exception as e:
            logger.error(f"Failed to update recipe like: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update recipe like"
            )

    async def update_comment(self, comment_id, comment, current_user):
        try:
            result = await self.recipe_dao.update_comment(comment_id, comment, current_user)
            return result
        except Exception as e:
            logger.error(f"service : Failed to update comment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update comment"
            )

    async def update_comment_like(self, comment_id, current_user):
        try:
            result = await self.recipe_dao.update_comment_like(comment_id, current_user)
            return result
        except Exception as e:
            logger.error(f"service : Failed to update comment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update comment"
            )
     # delete

    async def delete_one_recipe(self, recipe_id: str, current_user):
        try:
            result = await self.recipe_dao.delete_one_recipe(recipe_id, current_user)
            return result
        except Exception as e:
            logger.error(f"Failed to delete recipe: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to delete recipe"
            )

    async def delete_all_recipe(self):
        try:
            result = await self.recipe_dao.delete_all_recipe()
            return result
        except Exception as e:
            logger.error(f"Failed to delete all recipes: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to delete all recipes"
            )

    async def delete_comment(self, comment_id, current_user):
        try:
            result = await self.recipe_dao.delete_comment(comment_id, current_user)
            return result
        except Exception as e:
            logger.error(f"Failed to delete comment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to delete comment"
            )
