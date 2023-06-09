from pydantic import BaseModel
from datetime import datetime


class NotificationIn(BaseModel):
    user_id: str
    message: str
    timestamp: datetime
