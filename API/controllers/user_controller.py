from services.user_service import UserService
from dao.user_dao import UserDao
from models.user import UserIn, UserOut, LoginResponse, LoginRequest, LogoutRequest, LogoutResponse
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response

router = APIRouter()
user_dao = UserDao()
user_service = UserService(user_dao)


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    user_dao = UserDao()
    user_service = UserService(user_dao)
    user_id = await user_service.create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="사용자가 이미 존재합니다.")
    return {"user_id": user.user_id, "username": user.username, "email": user.email, "birth_date": user.birth_date, "img": user.img, "created_at": datetime.now()}


@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequest, response: Response):
    result = await user_service.login(user.user_id, user.password)
    if result:
        response.set_cookie(key="session_id", value=result["session_id"])
        return LoginResponse(message="로그인에 성공했습니다!", session_id=result["session_id"])
    else:
        raise HTTPException(status_code=400, detail="로그인에 실패했습니다.")


@router.post("/logout", response_model=LogoutResponse)
async def logout(logout_request: LogoutRequest):
    session_id = logout_request.session_id
    result = await user_service.logout(str(session_id))
    if result:
        return LogoutResponse(message="로그아웃에 성공하였습니다.")
    else:
        raise HTTPException(status_code=400, detail="로그아웃에 실패했습니다.")
