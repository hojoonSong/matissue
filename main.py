from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes.user_routes import user_router
from API.routes.recipe_routes import recipe_router
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import get_settings
import sys

settings = get_settings()

# 단일 연결 유지를 위한 전역 변수
db_client = None


def get_db_client():
    global db_client

    # 이미 연결된 클라이언트가 없는 경우에만 연결
    if not db_client:
        db_client = AsyncIOMotorClient(settings.mongo_db_url)

    return db_client


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스에서는 허용할 도메인을 명시적으로 설정하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users",
                   tags=["users"], dependencies=[Depends(get_db_client)])
app.include_router(recipe_router, prefix="/recipe",
                   tags=["recipe"], dependencies=[Depends(get_db_client)])
