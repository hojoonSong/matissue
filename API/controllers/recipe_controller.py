from fastapi import Depends, HTTPException, Path, Query, Response
from bson import json_util
from utils.config import get_settings
from utils.db_manager import MongoDBManager
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
from models.recipe_models import (
    CommentBase,
    CommentIn,
    CommentUpdate,
    RecipeBase,
    RecipeCreate,
    RecipeGetList,
    RecipeIn,
    RecipeUpdate,
)
from dao.recipe_dao import RecipeDao

from services.recipe_service import RecipeService
from utils.session_manager import SessionManager, get_current_session

router = APIRouter()
recipe_dao = RecipeDao()
recipe_service = RecipeService(recipe_dao)
settings = get_settings()
db_manager = MongoDBManager()
collection = db_manager.get_collection("recipes")


@router.get("/", response_model=RecipeGetList, tags=["recipes_get"])
async def get_all_recipes(page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_all_recipes(skip=skip_count, limit=limit)
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/categories", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_categories(
    value: str = Query(...), page: int = 1, limit: int = 160
):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_categories(
            value, skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/search", response_model=RecipeGetList, tags=["recipes_get"])
async def search_recipes(value: str, page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.search_recipes(value, skip=skip_count, limit=limit)
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/user",
    dependencies=[Depends(get_current_session)],
    response_model=RecipeGetList,
    tags=["recipes_get"],
)
async def get_recipes_by_current_user(
    current_user: str = Depends(get_current_session), page: int = 1, limit: int = 150
):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_user_id(
            current_user, skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content={"recipes":serialized_recipes})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/user/{user_id}", tags=["recipes_get"])
async def get_recipe_by_user_id(
    user_id: str, page: int = 1, limit: int = 150
):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_user_id(
            user_id, skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/popularity", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_popularity(page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_popularity(
            skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/latest", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_latest(page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_latest(
            skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/single", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_single_serving(page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_single_serving(
            skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/vegetarian", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_vegetarian(page: int = 1, limit: int = 160):
    try:
        skip_count = (page - 1) * limit
        recipes = await recipe_service.get_recipes_by_categories(
            category="vegetarian",skip=skip_count, limit=limit
        )
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/ingredients", response_model=RecipeGetList, tags=["recipes_get"])
async def get_recipes_by_ingredients(value: str):
    try:
        recipes = await recipe_service.get_recipes_by_ingredients(value)
        if len(recipes) == 0:
            return JSONResponse(content=[])
        serialized_recipes = json.loads(json.dumps(recipes, default=str))
        return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.get("/{recipe_id}", tags=["recipes_get"])
async def get_recipe_by_recipe_id(recipe_id: str):
    print('🍏')
    recipe = await recipe_service.get_recipe_by_recipe_id(recipe_id)
    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with id {recipe_id} not found"
        )
    comments = await recipe_service.get_comments(recipe_id)
    recipe['comments'] = comments
    await recipe_service.update_recipe_view(recipe_id)
    serialized_recipes = json.loads(json.dumps(recipe, default=str))
    return JSONResponse(content={"recipe": serialized_recipes})


@router.post(
    "/", dependencies=[Depends(get_current_session)], status_code=201, tags=["recipes"]
)
async def register_recipe(
    recipe: dict, current_user: str = Depends(get_current_session)
):
    try:
        recipe["user_id"] = current_user
        new_recipe = RecipeCreate(**recipe)  # dict를 RecipeCreate 클래스의 인스턴스로 변환
        result = await recipe_service.register_recipe(new_recipe)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to insert recipe")
        # serialized_recipes = json.loads(json.dumps(result, default=str))
        return Response(status_code=201)
        # return JSONResponse(content=serialized_recipes)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{recipe_id}",
    status_code=204,
    dependencies=[Depends(get_current_session)],
    tags=["recipes"],
)
async def delete_recipe(
    recipe_id: str, current_user: str = Depends(get_current_session)
):
    try:
        result = await recipe_service.delete_one_recipe(recipe_id, current_user)
        if result == 1:
            return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{recipe_id}", dependencies=[Depends(get_current_session)], tags=["recipes"]
)
async def update_recipe(
    recipe_id: str,
    updated_recipe: RecipeUpdate,
    current_user: str = Depends(get_current_session),
):
    try:
        existing_recipe = await recipe_service.get_recipe_to_update_recipe(recipe_id)
        if existing_recipe is None:
            raise HTTPException(
                status_code=404, detail=f"Recipe with id {recipe_id} not found"
            )
        updated_document = await recipe_service.update_recipe(recipe_id, updated_recipe, current_user)
        # serialized_recipe = json.loads(
        #     json.dumps(updated_document, default=str))
        return Response(status_code=201)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))


@router.patch(
    "/{recipe_id}/like",
    status_code=201,
    dependencies=[Depends(get_current_session)],
    tags=["recipes"],
)
async def update_like(recipe_id: str, current_user: str = Depends(get_current_session)):
    try:
        recipe = await recipe_service.update_recipe_like(recipe_id, current_user)
        if recipe is None:
            raise HTTPException(
                status_code=404, detail=f"Recipe with id {recipe_id} not found"
            )
        # serialized_recipe = json.loads(json.dumps(recipe, default=str))
        return Response(status_code=201)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))


@router.get("/comment/{comment_id}", tags=["comment"])
async def get_comments(comment_id: str):
    result = await recipe_service.get_one_comment(comment_id)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to find comment")
    serialized_comment = json.loads(json.dumps(result, default=str))
    return JSONResponse(content=serialized_comment, status_code=200)


@router.post(
    "/comment/{recipe_id}",
    dependencies=[Depends(get_current_session)],
    status_code=201,
    tags=["comment"],
)
async def register_comment(
    recipe_id: str, comment: CommentIn, current_user: str = Depends(get_current_session)
):
    try:
        result = await recipe_service.register_comment(recipe_id, comment, current_user)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to insert comment")
        # serialized_comment = json.loads(json.dumps(result, default=str))
        return Response(status_code=201)
        # return JSONResponse(content=serialized_comment, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/comment/{comment_id}",
    dependencies=[Depends(get_current_session)],
    tags=["comment"],
)
async def delete_comment(
    comment_id: str, current_user: str = Depends(get_current_session)
):
    try:
        result = await recipe_service.delete_comment(comment_id, current_user)
        if result == 0:
            raise HTTPException(status_code=500, detail="Failed to delete comment")
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/comment/{comment_id}",
    dependencies=[Depends(get_current_session)],
    tags=["comment"],
)
async def update_comment(
    comment_id: str,
    comment: CommentIn,
    current_user: str = Depends(get_current_session),
) -> CommentUpdate:
    try:
        result = await recipe_service.update_comment(comment_id, comment, current_user)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to update comment")
        # serialized_comment = json.loads(json.dumps(result, default=str))
        return Response(status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Controller:Failed to update comment{str(e)}"
        )


@router.patch(
    "/comment/{comment_id}/like",
    dependencies=[Depends(get_current_session)],
    tags=["comment"],
)
async def update_comment_like(
    comment_id: str, current_user: str = Depends(get_current_session)
) -> CommentUpdate:
    try:
        result = await recipe_service.update_comment_like(comment_id, current_user)
        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to update comment")
        # serialized_comment = json.loads(json.dumps(result, default=str))
        return Response(status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Controller:Failed to update comment{str(e)}"
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
