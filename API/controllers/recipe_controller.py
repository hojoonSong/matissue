from models.recipe import RecipeBase
from datetime import datetime
from fastapi import APIRouter, HTTPException
from uuid import UUID, uuid4
from utils.config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
settings = get_settings()

# 단일 연결 유지를 위한 전역 변수
db_client = None

router = APIRouter()

# 디비 클라이언트 연결
db_client = AsyncIOMotorClient(settings.mongo_db_url)
db = db_client[settings.mongo_db_name].get_collection("recipes")


@router.get("/")
async def yummy():
    return {"recipe": "😋"}


@router.get("/db")
async def fetch_db():
    return db.find().to_list(length=None)


@router.post("/db")
async def register_db(recipe: Recipe):
    await db.insert_one(recipe.dict())
    return {"recipe_title": recipe.recipe_title, "full": recipe}


@router.delete("/db/{recipe_id}")
async def delete_db(recipe_id: UUID):
    result = await db.delete_one({"recipe_id": recipe_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return {"msg": "success"}


@router.patch("/db/{recipe_id}")
async def update_db(recipe_id: UUID):
    result = await db.update_one({"recipe_id": recipe_id}, {"$set": recipe.dict()})
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return


@router.patch("/db/{recipe_title}/like")
async def update_like(recipe_id: UUID):
    update_query = {"$inc": {"recipe_like": 1}}
    result = await db.update_one({"recipe_title": recipe_title}, update_query)
    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    return
