from typing import List
from fastapi import WebSocket
from pydantic import BaseModel
from datetime import datetime


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: BaseModel):
        for connection in self.active_connections:
            await connection.send_json(message.dict())


class UserNotification(BaseModel):
    user_id: str
    message: str
    timestamp: datetime
