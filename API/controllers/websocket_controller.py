from fastapi import WebSocket, APIRouter, Path, WebSocketDisconnect
import aioredis
import asyncio
import json
import logging
from utils.config import get_settings

settings = get_settings()

router = APIRouter()

# WebSocket 연결 관리
active_connections = {}

# 로깅 설정
logging.basicConfig(level=logging.INFO)


@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str = Path(...)):
    await websocket.accept()
    active_connections[user_id] = websocket

    # Redis로부터 알림 받기
    async def listen_for_notifications():
        redis = aioredis.from_url(settings.redis_url)
        pubsub = redis.pubsub(ignore_subscribe_messages=True)
        await pubsub.subscribe("notifications")

        async def reader():
            async for message in pubsub.listen():
                if message["type"] == "message":
                    notification = json.loads(message["data"])
                    target_user_id = notification["user_id"]
                    if target_user_id in active_connections:
                        target_websocket = active_connections[target_user_id]
                        await target_websocket.send_text(notification["message"])

                        # 서버 로그에 메시지 전송 로그 출력
                        logging.info(
                            f"메시지를 전송하였습니다. {target_user_id}: {notification['message']}"
                        )

        reader_task = asyncio.create_task(reader())
        await reader_task
        await pubsub.unsubscribe("notifications")
        redis.close()
        await redis.wait_closed()

    # 별도의 코루틴으로 Redis 알림 수신 시작
    listen_task = asyncio.create_task(listen_for_notifications())

    # Keep-Alive: 주기적으로 ping 메시지 전송
    async def keep_alive(websocket):
        while True:
            try:
                await websocket.ping()
                await asyncio.sleep(30)  # 30초마다 ping 메시지 전송
            except:
                break

    # Keep-Alive 태스크 시작
    asyncio.create_task(keep_alive(websocket))

    # WebSocket 연결 유지
    try:
        while True:
            data = await websocket.receive_text()
            # 클라이언트로부터 받은 데이터를 처리하는 로직을 여기에 추가할 수 있습니다.
    except WebSocketDisconnect:
        logging.info(f"WebSocket disconnected: {user_id}")
    finally:
        active_connections.pop(user_id)
        listen_task.cancel()  # Redis listener task를 취소합니다.
