from services.user_service import UserService
from dao.user_dao import UserDao
from models.user import UserUpdate, UserIn, UserOut
from models.response_models import LoginResponse, LoginRequest, LogoutRequest, MessageResponse, DeleteRequest
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, Depends
from utils.session_manager import get_current_session
from utils.permission_manager import check_user_permissions
from utils.response_utils import common_responses

router = APIRouter()
user_dao = UserDao()
user_service = UserService(user_dao)


@router.post("/", response_model=UserOut, status_code=201, responses=common_responses)
async def create_user(user: UserIn):
    user_id = await user_service.create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="사용자가 이미 존재합니다.")
    return {"user_id": user.user_id, "username": user.username, "email": user.email, "birth_date": user.birth_date, "img": user.img, "created_at": datetime.now()}


@router.put("/", response_model=UserOut, dependencies=[Depends(get_current_session)], responses=common_responses)
async def update_user(user: UserUpdate, current_user: str = Depends(get_current_session)):
    check_user_permissions(user.user_id, current_user)

    user_in_db = UserUpdate(**user.dict(), hashed_password='')
    updated = await user_service.update_user(user_in_db)
    if not updated:
        raise HTTPException(status_code=400, detail="사용자 정보 업데이트에 실패하였습니다.")
    updated_user = await user_dao.get_user_by_id(user.user_id)
    return {"user_id": updated_user.user_id,
            "username": updated_user.username,
            "email": updated_user.email,
            "birth_date": updated_user.birth_date,
            "img": updated_user.img,
            "created_at": updated_user.created_at}


@router.delete("/", response_model=MessageResponse, dependencies=[Depends(get_current_session)], responses=common_responses)
async def delete_user(user: DeleteRequest, current_user: str = Depends(get_current_session)):
    check_user_permissions(user.user_id, current_user)
    result = await user_service.delete_user(user.user_id, user.password, str(user.session_id))
    if not result:
        raise HTTPException(status_code=400, detail="사용자 탈퇴에 실패하였습니다.")

    return MessageResponse(message="성공적으로 탈퇴되었습니다!")


@router.post("/login", response_model=LoginResponse, responses=common_responses)
async def login(user: LoginRequest, response: Response):
    result = await user_service.login(user.user_id, user.password)
    if result:
        response.set_cookie(key="session_id", value=result["session_id"])
        return LoginResponse(message="로그인에 성공했습니다!", session_id=result["session_id"])
    else:
        raise HTTPException(status_code=400, detail="로그인에 실패했습니다.")


@router.post("/logout", response_model=MessageResponse, dependencies=[Depends(get_current_session)], responses=common_responses)
async def logout(logout_request: LogoutRequest):
    session_id = logout_request.session_id
    result = await user_service.logout(str(session_id))
    if result:
        return MessageResponse(message="로그아웃에 성공하였습니다.")
    else:
        raise HTTPException(status_code=400, detail="로그아웃에 실패했습니다.")


@router.post("/me", response_model=UserOut, dependencies=[Depends(get_current_session)], responses=common_responses)
async def get_user(current_user: str = Depends(get_current_session)):
    user_in_db = await user_dao.get_user_by_id(current_user)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return {
        "user_id": user_in_db.user_id,
        "username": user_in_db.username,
        "email": user_in_db.email,
        "birth_date": user_in_db.birth_date,
        "img": user_in_db.img,
        "created_at": user_in_db.created_at
    }


@router.get("/", dependencies=[Depends(get_current_session)], responses=common_responses)
async def get_users(current_user: str = Depends(get_current_session)):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    users = await user_dao.get_users()
    return users
