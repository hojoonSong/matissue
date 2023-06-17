from fastapi import APIRouter
from API.controllers import verify_controller

verify_router = APIRouter()

verify_router.include_router(verify_controller.router)
