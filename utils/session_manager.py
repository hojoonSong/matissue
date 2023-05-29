import uuid
import redis
from typing import Any
from fastapi import HTTPException
from .config import get_settings

settings = get_settings()

r = redis.Redis.from_url(settings.redis_url, decode_responses=True)

class SessionManager:
    def create_session(self, data: Any):
        session_id = str(uuid.uuid4())
        r.set(session_id, data)
        return session_id

    def get_session(self, session_id: str):
        data = r.get(session_id)
        if data is None:
            raise HTTPException(status_code=401, detail="Invalid session id")
        return data

    def delete_session(self, session_id: str):
        r.delete(session_id)
