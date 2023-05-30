# 서버 의존성
from typing import List
from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

# 응답 의존성
from fastapi.responses import JSONResponse
import json
# 유틸
from utils.config import get_settings
from utils.db_manager import MongoDBManager
# 계층
from models.recipe import Recipe
from dao.recipe_dao import RecipeDao

# 디비연결
settings = get_settings()
db_client = None
db_client = AsyncIOMotorClient(settings.mongo_db_url)
db = db_client[settings.mongo_db_name].get_collection("recipes")

router = APIRouter()

""" 
dao 진행
"""

# 모든 레시피 가져오기


@router.get("/")
async def get_all_recipes():
    dao = RecipeDao()
    try:
        recipes = await dao.get_all_recipe()
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

""" 
계층 분리 전
"""

# 레시피 하나 포스팅하기


@router.post("/")
async def register_recipe(recipe: Recipe):
    await db.insert_one(recipe.dict())
    return {"recipe_title": recipe.recipe_title, "full": recipe}, 200

# 레시피 여러개 포스팅하기


@router.post("/many")
async def register_recipes(recipes: List[Recipe]):
    recipe_data = [recipe.dict() for recipe in recipes]
    result = await db.insert_many(recipe_data)
    if len(result.inserted_ids) != len(recipe_data):
        raise HTTPException(
            status_code=500,
            detail="Error occurred while inserting recipes"
        )
    return {"message": "Recipes inserted successfully"}, 200

# 레시피 하나 삭제하기


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str):
    result = await db.delete_one({"recipe_id": recipe_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return {"msg": "삭제성공"}, 204

# 레시피 하나 수정하기


@router.patch("/{recipe_id}")
async def update_recipe(recipe_id: str):
    result = await db.update_one({"recipe_id": recipe_id}, {"$set": recipe.dict()})
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return {"msg": "success"}, 200

# 레시피 좋아요 클릭시


@router.patch("/{recipe_id}/like")
async def update_like(recipe_id: str):
    update_query = {"$inc": {"recipe_like": 1}}
    result = await db.update_one({"recipe_id": recipe_id}, update_query)
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return {"msg": "success"}, 200
