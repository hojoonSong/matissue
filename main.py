from fastapi import FastAPI
from API.routes.user_routes import user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
