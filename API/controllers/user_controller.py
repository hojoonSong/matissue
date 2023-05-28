from services.user_service import UserService
from dao.user_dao import UserDao
from models.user import UserIn, UserOut
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    user_dao = UserDao()
    user_service = UserService(user_dao)
    user_id = await user_service.create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"user_id": user.user_id, "username": user.username, "email": user.email, "created_at": datetime.now()}
