from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.routes.api_routes import api_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://www.matissue.com/",
    "https://www.matissue.com",
    "https://matissue.com/",
    "https://matissue.com",
    "https://matissue.onrender.com",
    "https://matissue-1jim.onrender.com",
    "https://kdt-sw-4-team10.elicecoding.com",
    "https://kdt-sw-4-team10.elicecoding.com/",
    "https://matissue.p-e.kr/",
    "https://matissue.p-e.kr",
    "https://mat-issue.onrender.com/",
    "https://mat-issue.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 실제 서비스에서는 허용할 도메인을 명시적으로 설정하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
