from services.user_service import UserService
from dao.user_dao import UserDao
from models.user import UserIn, UserOut, LoginResponse, LoginRequest
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response
from dao.user_dao import UserDao

router = APIRouter()
user_dao = UserDao()
user_service = UserService(user_dao)


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    user_dao = UserDao()
    user_service = UserService(user_dao)
    user_id = await user_service.create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"user_id": user.user_id, "username": user.username, "email": user.email, "birth_date": user.birth_date, "created_at": datetime.now()}


@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequest, response: Response):
    result = await user_service.login(user.user_id, user.password)
    if result:
        response.set_cookie(key="session_id", value=result["session_id"])
        return LoginResponse(message="로그인에 성공했습니다!", session_id=result["session_id"])
    else:
        raise HTTPException(status_code=400, detail="로그인에 실패했습니다.")
