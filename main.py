from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes.api_routes import api_router

import sys


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스에서는 허용할 도메인을 명시적으로 설정하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
