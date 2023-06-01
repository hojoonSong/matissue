from fastapi import APIRouter
from API.routes.user_routes import user_router
from API.routes.recipe_routes import recipe_router

api_router = APIRouter()

api_router.include_router(user_router, prefix="/users",
                          tags=["users"])
api_router.include_router(recipe_router, prefix="/recipes",
                          tags=["recipes"])
