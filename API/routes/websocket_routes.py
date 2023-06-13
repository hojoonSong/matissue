from fastapi import APIRouter
from API.controllers import websocket_controller

websocket_router = APIRouter()

websocket_router.include_router(websocket_controller.router)
