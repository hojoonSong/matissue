from fastapi import FastAPI
from API.routes.api_routes import api_router

import sys


# 캐시 폴더 경로 설정
new_cache_dir = "/fastcache"

# sys.path에 캐시 폴더 경로 추가
sys.path.insert(0, new_cache_dir)

app = FastAPI()

app.include_router(api_router, prefix="/api", tags=["api"])
