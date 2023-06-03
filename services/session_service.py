import redis
from uuid import uuid4
from typing import Optional
from utils.config import get_settings

settings = get_settings()

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)


class SessionService:
    def __init__(self, r):
        self.redis = redis.Redis(r)

    def create_session(self, user_id: str) -> str:
        session_id = str(uuid4())
        self.redis.set(session_id, user_id)
        return session_id

    def get_id_from_session(self, session_id: str) -> Optional[str]:
        user_id = self.redis.get(session_id)
        return user_id
