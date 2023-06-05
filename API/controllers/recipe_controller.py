from fastapi import HTTPException, Query
from bson import json_util
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
from models.recipe_models import RecipeBase, RecipeCreate, RecipeGetMany, RecipeGetOne
from dao.recipe_dao import RecipeDao
from services.recipe_service import RecipeService

router = APIRouter()
service = RecipeService()

# @router.get("/")
# async def get_all_recipes(page: int = Query(1, ge=1), limit: int = Query(16, ge=1, le=100)):
#     try:
#         # 페이지와 limit 값을 기반으로 offset을 계산합니다.
#         offset = (page - 1) * limit
#         # 계산된 offset과 limit을 사용하여 레시피를 가져옵니다.
#         recipes = await dao.get_all_recipes(offset=offset, limit=limit)
#         # 레시피를 직렬화합니다.
#         serialized_recipes = json.loads(json.dumps(recipes, default=str))
#         return JSONResponse(content=serialized_recipes)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_recipes_by_categories(value: str):
    try:
        recipes = await dao.get_recipes_by_categories(value)
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# @router.get("/")
# async def get_all_recipes():
#     try:
#         recipes = await dao.get_all_recipes()
#         serialized_recipes = json.loads(json.dumps(recipes, default=str))
#         return JSONResponse(content=serialized_recipes)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/search")
async def search_recipes_by_title(value: str):
    pipeline = [
        {"$match": {
            "$or": [
                {"recipe_title": {"$regex": value, "$options": "i"}},
                {"recipe_category": {"$regex": value, "$options": "i"}},
                {"recipe_info": {"$regex": value, "$options": "i"}},
                {"recipe_ingredients.name": {"$regex": value, "$options": "i"}}
            ]
        }}
    ]
    result_cursor = collection.aggregate(pipeline)
    result = []
    async for document in result_cursor:
        result.append(json_util.loads(json_util.dumps(document)))
    if not result:
        raise HTTPException(status_code=404, detail="No recipes found")
    serialized_recipes = json.loads(json.dumps(result, default=str))
    return JSONResponse(content=serialized_recipes)


@router.get("/{recipe_id}")
async def get_recipe_by_recipe_id(recipe_id: str):
    try:
        recipe = await dao.get_recipe_by_recipe_id(recipe_id)
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        await dao.update_recipe_view(recipe_id)
        serialized_recipes = json.loads(json.dumps(recipe, default=str))
        return JSONResponse(content=serialized_recipes), 200
    except HTTPException as e:
        raise e
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/user/{user_id}", response_model=RecipeGetMany)
async def get_recipes_by_user_id(user_id: str):
    recipe = await dao.get_recipes_by_user_id(user_id)
    print(recipe)
    return ({"recipes": recipe})


@router.post("/")
async def register_recipe(recipe: RecipeCreate):
    try:
        result = await dao.register_recipe(recipe)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to insert recipe")
        return {"recipe_id": result['recipe_id']}, 200
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/many")
async def register_recipes(recipes: List[RecipeCreate]):
    response = await dao.register_recipes(recipes)
    return response, 200


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str):
    result = await dao.delete_one_recipe(recipe_id)
    if result == 1:
        return {"msg": "삭제 성공"}, 204
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )


@router.delete("/")
async def delete_all_recipe():
    result = await dao.delete_all_recipe()
    if result == 1:
        return {"msg": "삭제 성공"}, 204
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Can't delete recipes"
        )


@router.patch("/{recipe_id}")
async def update_recipe(recipe_id: str, updated_recipe: RecipeBase):
    try:
        updated_document = await dao.update_recipe(recipe_id, updated_recipe)
        updated_document_dict = updated_document.copy()
        updated_document_dict.pop("_id")  # ObjectId 필드 삭제
        return JSONResponse(content=updated_document_dict)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e.detail)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.patch("/{recipe_id}/like")
async def update_like(recipe_id: str):
    try:
        recipe = await dao.get_recipe_by_id(recipe_id)
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        await dao.update_recipe_like(recipe_id)
        serialized_recipe = json.loads(json.dumps(recipe, default=str))
        return serialized_recipe

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
