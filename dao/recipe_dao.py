from dao.user_dao import UserDao
from typing import List
from fastapi import HTTPException

from pymongo import ReturnDocument
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from models.recipe_models import CommentBase, CommentUpdate, RecipeBase, RecipeUpdate, RecipeView, RecipeLike, RecipeCreate
from datetime import datetime
settings = get_settings()


class RecipeDao:
    def __init__(self, db_manager: MongoDBManager = None):
        self.db_manager = db_manager or MongoDBManager()
        self.collection = self.db_manager.get_collection("recipes")
        self.user_collection = self.db_manager.get_collection("users")
        self.comment_collection = self.db_manager.get_collection("comments")

    # get

    # async def get_all_recipes(self, skip: int = 0, limit: int = 160):
    #     cursor = self.collection.find({}).sort("created_at", -1).skip(skip).limit(limit)
    #     result = await cursor.to_list(length=None)
    #     return result

    async def get_all_recipes_with_comments(self, skip: int = 0, limit: int = 160):
        pipeline = [
            {"$sort": {"created_at": -1}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$lookup": {
                    "from": "comments",
                    "localField": "recipe_id",
                    "foreignField": "comment_parent",
                    "as": "comments"
                }
            }
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result

    # async def get_recipes_by_categories(self, category, skip: int = 0, limit: int = 160):
    #     result = await self.collection.find({"recipe_category": category}).sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
    #     return result
    async def get_recipes_by_categories_with_comments(self, category, skip: int = 0, limit: int = 160):
        pipeline = [
            {"$match": {"recipe_category": category}},
            {"$sort": {"created_at": -1}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$lookup": {
                    "from": "comments",
                    "localField": "recipe_id",
                    "foreignField": "comment_parent",
                    "as": "comments"
                }
            }
        ]
        result = await self.collection.aggregate(pipeline).to_list(length=None)
        return result
    
    async def get_recipes_by_popularity(self, skip: int = 0, limit: int = 160):
        pipeline = [
            {
                "$addFields": {
                    "recipe_like_length": { "$size": "$recipe_like" }
                }
            },
            {
                "$sort": { "recipe_like_length": -1 }
            },
            {
                "$project": {
                    "recipe_like_length": 0
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        results = results[skip:skip+limit]  # 페이지네이션을 위해 결과를 잘라냄
        return results

    async def get_recipes_by_latest(self, skip: int = 0, limit: int = 160):
        results = await self.collection.find().sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
        return results
    
    async def get_recipes_by_user_id(self, user_id, skip: int = 0, limit: int = 160):
        result = await self.collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
        return result
    
    async def get_recipes_by_single_serving(self, skip: int = 0, limit: int = 160):
        results = await self.collection.find({"recipe_info.serving": 1}).sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
        return results

    async def get_recipes_by_vegetarian(self, skip: int = 0, limit: int = 160):
        results = await self.collection.find({"recipe_category": "vegetarian"}).sort("created_at", -1).skip(skip).limit(limit).to_list(length=None)
        return results

    async def get_recipes_by_ingredients(self, value):
        pipeline = [
            {"$match": {
                "$or": [
                    {"recipe_ingredients.name": {"$regex": value, "$options": "i"}}
                ]
            }}
        ]
        results = await self.collection.aggregate(pipeline).to_list(length=None)
        return results
    
    async def get_recipe_by_recipe_id(self, recipe_id):
        recipe = await self.collection.find_one({"recipe_id": recipe_id})
        # user = await self.user_collection.find_one({"user_id": recipe["user_id"]})
        # recipe['user_img'] = user["img"]
        # recipe['user_fan'] = len(user.get('fans', []))
        # recipe['user_subscription'] = len(user.get('subscription', []))
        return recipe

    async def get_recipe_to_update_recipe(self, id):
        result = await self.collection.find_one({"recipe_id": id})
        if result is None:
            return None
        return RecipeCreate(**result)

    async def get_comments(self, recipe_id):
        result = await self.comment_collection.find({"comment_parent": recipe_id}).to_list(length=None)
        return result

    # post

    async def register_recipe(self, recipe: RecipeCreate):
        user = await self.user_collection.find_one({"user_id": recipe.user_id})
        user_nickname = user["username"]
        recipe.user_nickname = user_nickname
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

    async def update_recipe(self, recipe_id: str, updated_recipe, current_user):
        existing_recipe = await self.collection.find_one({"recipe_id": recipe_id})
        if existing_recipe['user_id'] != current_user:
            raise HTTPException(
                status_code=403,
                detail="작성자가 아닐 시 수정이 불가합니다."
            )
        modified_recipe = RecipeUpdate(
            recipe_title=updated_recipe.recipe_title,
            recipe_thumbnail=updated_recipe.recipe_thumbnail,
            recipe_video=updated_recipe.recipe_video,
            recipe_description=updated_recipe.recipe_description,
            recipe_category=updated_recipe.recipe_category,
            recipe_info=updated_recipe.recipe_info,
            recipe_ingredients=updated_recipe.recipe_ingredients,
            recipe_sequence=updated_recipe.recipe_sequence,
            recipe_tip=updated_recipe.recipe_tip,
            user_nickname=existing_recipe["user_nickname"]
        )
        updated_document = await self.collection.find_one_and_update(
            {"recipe_id": recipe_id},
            {"$set": modified_recipe.dict()},
            return_document=ReturnDocument.AFTER
        )
        if updated_document is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        return updated_document

    # delete

    async def delete_one_recipe(self, recipe_id: str, current_user):
        existing_recipe = await self.collection.find_one({"recipe_id": recipe_id})
        if existing_recipe['user_id'] != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to delete this recipe"
            )
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

    async def update_recipe_view(self, recipe_id: str):
        update_query = {"$inc": {"recipe_view": 1}}
        result = await self.collection.update_one({"recipe_id": recipe_id}, update_query)
        return result.modified_count

    async def update_recipe_like(self, recipe_id: str, current_user):
        existing_recipe = await self.collection.find_one({"recipe_id": recipe_id})
        recipe_like = existing_recipe.get("recipe_like", [])
        if current_user in recipe_like:
            recipe_like.remove(current_user)
        else:
            recipe_like.append(current_user)
        updated_comment = await self.collection.find_one_and_update(
            {"recipe_id": recipe_id},
            {"$set": {"recipe_like": recipe_like}},
            return_document=ReturnDocument.AFTER
        )
        return updated_comment

    async def get_one_comment(self, comment_id):
        result = await self.comment_collection.find_one({"comment_id": comment_id})
        return result

    async def register_comment(self, recipe_id, comment: CommentBase, current_user):
        user = await self.user_collection.find_one({"user_id": current_user})
        comment_author = current_user
        comment_nickname = user["username"]
        comment_parent = recipe_id
        comment_text = comment.comment_text
        comment_profile_img = user["img"]
        comment_base = CommentBase(
            comment_author=comment_author,
            comment_text=comment_text,
            comment_parent=comment_parent,
            comment_nickname=comment_nickname,
            comment_profile_img=comment_profile_img
        )
        inserted_data = await self.comment_collection.insert_one(comment_base.dict())
        # await self.comment_collection.find_one({"comment_id": comment_base.comment_id})
        return inserted_data

    async def update_comment(self, comment_id, modified_comment, current_user):
        existing_comment = await self.comment_collection.find_one({"comment_id": comment_id})
        if existing_comment:
            current_user = existing_comment['comment_author']
        else:
            raise HTTPException(
                status_code=404,
                detail="댓글이 존재하지 않습니다"
            )
        if existing_comment['comment_author'] != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to update this comment"
            )
        user = await self.user_collection.find_one({"user_id": current_user})
        comment_nickname = user["username"]
        comment_profile_img = user["img"]
        comment_text = modified_comment.comment_text
        update_data = CommentUpdate(
            comment_text=comment_text,
            comment_nickname=comment_nickname,
            comment_profile_img=comment_profile_img
        )
        updated_comment = await self.comment_collection.find_one_and_update(
            {"comment_id": comment_id},
            {"$set": update_data.dict()},
            return_document=ReturnDocument.AFTER
        )
        return updated_comment

    async def update_comment_like(self, comment_id, current_user):
        existing_comment = await self.comment_collection.find_one({"comment_id": comment_id})
        comment_like = existing_comment.get("comment_like", [])
        if current_user in comment_like:
            comment_like.remove(current_user)
        else:
            comment_like.append(current_user)
        updated_comment = await self.comment_collection.find_one_and_update(
            {"comment_id": comment_id},
            {"$set": {"comment_like": comment_like}},
            return_document=ReturnDocument.AFTER
        )
        return updated_comment

    async def delete_comment(self, comment_id: str, current_user):
        existing_comment = await self.comment_collection.find_one({"comment_id": comment_id})
        if existing_comment is None:
            raise HTTPException(
                status_code=404,
                detail="Comment not found"
            )
        if existing_comment['comment_author'] != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to delete this comment"
            )
        result = await self.comment_collection.delete_one({"comment_id": comment_id})
        if result.deleted_count == 1:
            return 1  # 문서가 성공적으로 삭제되었을 경우
        else:
            return 0  # 문서 삭제 실패

    #    페이지 네이션
    #     return result
    # async def get_all_recipes(self, offset=0, limit=16):
    #     result = await self.collection.find().skip(offset).limit(limit).to_list(length=None)
    #     return result
