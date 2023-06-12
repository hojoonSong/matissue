import redis
import json
from .config import get_settings

settings = get_settings()

# Redis pub/sub 설정
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe("notifications")


# NotificationManager 클래스
class NotificationManager:
    @staticmethod
    def send_notification(user_id: str, message: str):
        notification = {"user_id": user_id, "message": message}
        redis_client.publish("notifications", json.dumps(notification))
