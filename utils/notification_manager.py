import json
import logging
import aioredis
from .config import get_settings

settings = get_settings()


# NotificationManager 클래스
class NotificationManager:
    def __init__(self):
        self.redis = None
        self.pubsub = None

    async def initialize(self):
        # aioredis 2.x 이상에서는 create_redis_pool 함수 대신 from_url 함수를 사용합니다.
        self.redis = await aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)

        # Create a pubsub instance
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe("notifications")

    async def send_notification(self, user_id: str, message: str):
        notification = {"user_id": user_id, "message": message}

        # 메시지 발행 전 로그 출력
        logging.info(f"사용자 {user_id}에게 : {message}라고 전송하였습니다.")

        # Publish the message
        await self.redis.publish("notifications", json.dumps(notification))

    async def close(self):
        if self.pubsub:
            await self.pubsub.unsubscribe("notifications")
            self.pubsub.close()
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()


async def get_notification_manager():
    notification_manager = NotificationManager()
    await notification_manager.initialize()
    return notification_manager
