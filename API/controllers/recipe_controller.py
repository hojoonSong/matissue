from fastapi import Depends, HTTPException, Path, Query
from bson import json_util
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
from models.recipe_models import CommentBase, CommentIn, RecipeBase, RecipeCreate, RecipeGetList, RecipeUpdate
from dao.recipe_dao import RecipeDao
from services.recipe_service import RecipeService
from utils.session_manager import SessionManager, get_current_session, get_current_user

router = APIRouter()
recipe_dao = RecipeDao()
recipe_service = RecipeService(recipe_dao)
settings = get_settings()
db_manager = MongoDBManager()
collection = db_manager.get_collection("recipes")


@router.get("/", response_model=RecipeGetList)
async def get_all_recipes():
    try:
        recipes = await recipe_service.get_all_recipes()
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/categories", response_model=RecipeGetList)
async def get_recipes_by_categories(value: str = Query(...)):
    try:
        recipes = await recipe_service.get_recipes_by_categories(value)
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/search", response_model=RecipeGetList)
async def search_recipes_by_title(value: str):
    pipeline = [
        {"$match": {
            "$or": [
                {"recipe_title": {"$regex": value, "$options": "i"}},
                {"recipe_category": {"$regex": value, "$options": "i"}},
                {"recipe_description": {"$regex": value, "$options": "i"}},
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


@router.get("/user", dependencies=[Depends(get_current_session)])
async def get_recipes_by_user_id(current_user: str = Depends(get_current_session)):
    recipes = await recipe_service.get_recipes_by_user_id(current_user)
    return JSONResponse(content={"recipes": recipes})


@router.get("/popularity", response_model=RecipeGetList)
async def get_recipes_by_popularity():
    recipe = await recipe_service.get_recipes_by_popularity()
    return JSONResponse(content={"recipes": recipe})


@router.get("/{recipe_id}")
async def get_recipe_by_recipe_id(recipe_id: str):
    recipe = await recipe_service.get_recipe_by_recipe_id(recipe_id)
    comments = await recipe_dao.get_comments(recipe_id)
    recipe['comments'] = comments
    print(comments)
    print(recipe)
    if recipe == None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    await recipe_service.update_recipe_view(recipe_id)
    serialized_recipes = json.loads(json.dumps(recipe, default=str))
    return JSONResponse(content={"recipe": serialized_recipes})


@router.post("/", dependencies=[Depends(get_current_session)], status_code=201)
async def register_recipe(recipe: RecipeCreate, current_user: str = Depends(get_current_session)) -> RecipeCreate:
    try:
        recipe["user_id"] = current_user
        result = await recipe_service.register_recipe(recipe)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to insert recipe")
        serialized_recipes = json.loads(json.dumps(result, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/many", status_code=201)
async def register_recipes(recipes: List[RecipeCreate]):
    response = await recipe_service.register_recipes(recipes)
    return JSONResponse(content=response, status_code=201)


@router.get("/comment/{comment_id}")
async def get_comments(comment_id: str):
    try:
        result = await recipe_dao.get_one_comment(comment_id)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to find comment")
        serialized_comment = json.loads(json.dumps(result[0], default=str))
        return JSONResponse(content=serialized_comment, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/comment/{recipe_id}")
async def register_comment(recipe_id: str, comment: CommentIn):
    try:
        result = await recipe_dao.register_comment(recipe_id, comment)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to insert comment")
        serialized_comment = json.loads(json.dumps(result, default=str))
        return JSONResponse(content=serialized_comment, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.patch("/comment/{comment_id}")
async def update_comment(comment_id: str, comment: CommentIn):
    try:
        result = await recipe_dao.update_comment(comment_id, comment)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to update comment")
        serialized_comment = json.loads(json.dumps(result, default=str))
        return JSONResponse(content=serialized_comment, status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: str):
    try:
        result = await recipe_dao.delete_comment(comment_id)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to delete comment")
        return JSONResponse(status_code=204)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: str):
    result = await recipe_service.delete_one_recipe(recipe_id)
    if result == 1:
        return JSONResponse(status_code=204)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )


@router.patch("/{recipe_id}")
async def update_recipe(recipe_id: str, updated_recipe: RecipeUpdate):
    try:
        existing_recipe = await recipe_dao.get_recipe_to_update_recipe(recipe_id)
        if existing_recipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        # 원래 가지고 있는 값으로 업데이트할 필드들 설정
        updated_recipe.recipe_id = existing_recipe.recipe_id
        updated_recipe.recipe_view = existing_recipe.recipe_view
        updated_recipe.user_id = existing_recipe.user_id
        updated_recipe.created_at = existing_recipe.created_at
        updated_recipe.recipe_like = existing_recipe.recipe_like
        updated_document = await recipe_dao.update_recipe(recipe_id, updated_recipe)
        updated_document_dict = updated_document.copy()
        updated_document_dict.pop("_id")  # ObjectId 필드 삭제
        updated_document_dict["created_at"] = updated_document_dict["created_at"].isoformat(
        )
        serialized_recipe = json.loads(
            json.dumps(updated_document_dict, default=str))
        return JSONResponse(content=serialized_recipe, status_code=201)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e.detail)
        )


@router.patch("/{recipe_id}/like", status_code=201)
async def update_like(recipe_id: str):
    try:
        recipe = await recipe_service.update_recipe_like(recipe_id)
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Recipe with id {recipe_id} not found"
            )
        serialized_recipe = json.loads(json.dumps(recipe, default=str))
        return JSONResponse(content=serialized_recipe, status_code=201)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=str(e.detail)
        )

# 페이지네이션
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


# 위험
# @router.delete("/", status_code=204)
# async def delete_all_recipe():
#     result = await recipe_service.delete_all_recipe()
#     if result == 1:
#         return {"msg": "삭제 성공"}
#     else:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Can't delete recipes"
#         )
