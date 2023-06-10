from fastapi import APIRouter, WebSocket
from utils.websocket_manager import WebSocketManager, UserNotification
from starlette.websockets import WebSocketDisconnect
from datetime import datetime

router = APIRouter()
websocket_manager = WebSocketManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 웹소켓으로부터 데이터를 수신하고 필요한 처리를 수행합니다.
            await websocket_manager.send_message(
                UserNotification(
                    user_id=user_id, message="알림을 보냅니다.", timestamp=datetime.now()
                )
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
