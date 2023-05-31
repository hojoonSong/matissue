from fastapi import Depends, FastAPI
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


# 캐시 폴더 경로 설정
new_cache_dir = "/fastcache"

# sys.path에 캐시 폴더 경로 추가
sys.path.insert(0, new_cache_dir)

app = FastAPI()


app.include_router(user_router, prefix="/users",
                   tags=["users"], dependencies=[Depends(get_db_client)])
app.include_router(recipe_router, prefix="/recipe",
                   tags=["recipe"], dependencies=[Depends(get_db_client)])
