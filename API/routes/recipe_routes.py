from fastapi import APIRouter
from API.controllers import recipe_controller

recipe_router = APIRouter()

recipe_router.include_router(recipe_controller.router)
