from fastapi import FastAPI
from API.routes.user_routes import user_router
from API.routes.recipe_routes import recipe_router
import sys

# 캐시 폴더 경로 설정
new_cache_dir = "/fastcache"

# sys.path에 캐시 폴더 경로 추가
sys.path.insert(0, new_cache_dir)

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(recipe_router, prefix="/recipe", tags=["recipe"])
