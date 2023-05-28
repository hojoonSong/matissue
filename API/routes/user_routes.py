from fastapi import APIRouter
from API.controllers import user_controller

user_router = APIRouter()

user_router.include_router(user_controller.router)
