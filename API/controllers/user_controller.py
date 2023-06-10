from services.user_service import UserService, get_user_service
from dao.user_dao import UserDao
from models.user_models import UserUpdate, UserIn, UserOut, UserInDB
from models.response_models import (
    LoginResponse,
    LoginRequest,
    MessageResponse,
    PeopleResponse,
)
from fastapi import APIRouter, HTTPException, Response, Depends, Query, Request
from typing import List
from utils.session_manager import (
    SessionManager,
    get_current_session,
    get_verification_link,
)
from utils.permission_manager import check_user_permissions
from utils.response_manager import common_responses
from utils.email_manager import send_verification_email

router = APIRouter()
user_dao = UserDao()
user_service = UserService(user_dao)
session_manager = SessionManager()


@router.post("/", status_code=201, responses=common_responses)
async def create_user(
    user: UserIn, session_manager: SessionManager = Depends(SessionManager)
):
    await user_service.validate_user_creation(user)

    verification_code = session_manager.create_verification_code(user.email)
    verification_link = get_verification_link(user.email, verification_code)

    send_verification_email(user.email, verification_link)

    await session_manager.save_user_info(user)

    return {"message": "인증 이메일이 발송되었습니다. 이메일을 확인해 주세요."}


@router.patch(
    "/",
    response_model=UserOut,
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def update_user(
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: str = Depends(get_current_session),
):
    return await user_service.update_user(user, current_user)


@router.delete(
    "/",
    response_model=MessageResponse,
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def delete_user(
    user: LoginRequest,
    request: Request,
    current_user: str = Depends(get_current_session),
):
    session_id = request.cookies.get("session-id")
    check_user_permissions(user.user_id, current_user)
    result = await user_service.delete_user(
        user.user_id, user.password, str(session_id)
    )
    if not result:
        raise HTTPException(status_code=400, detail="사용자 탈퇴에 실패하였습니다.")

    return MessageResponse(message="성공적으로 탈퇴되었습니다!")


@router.post("/login", response_model=LoginResponse, responses=common_responses)
async def login(user: LoginRequest, response: Response):
    result = await user_service.login(user.user_id, user.password)
    if result:
        response.set_cookie(
            key="session-id",
            value=result["session_id"],
            secure="None",
            httponly="True",
            samesite="None",
        )
        return LoginResponse(message="로그인에 성공했습니다!", session_id=result["session_id"])
    raise HTTPException(status_code=400, detail="로그인에 실패했습니다.")


@router.post(
    "/logout",
    response_model=MessageResponse,
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session-id")
    if session_id is None:
        raise HTTPException(status_code=400, detail="세션 ID를 찾을 수 없습니다")

    result = await user_service.logout(session_id, response)

    if result["detail"] == "성공적으로 로그아웃되었습니다.":
        return MessageResponse(message=result["detail"])

    raise HTTPException(status_code=400, detail="로그아웃에 실패했습니다.")


@router.get(
    "/me",
    response_model=UserOut,
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def get_user(current_user: str = Depends(get_current_session)):
    user_in_db = await user_dao.get_user_by_id(current_user)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user_in_db.user_id,
        "username": user_in_db.username,
        "email": user_in_db.email,
        "birth_date": user_in_db.birth_date,
        "img": user_in_db.img,
        "created_at": user_in_db.created_at,
    }


@router.get(
    "/", dependencies=[Depends(get_current_session)], responses=common_responses
)
async def get_users(
    current_user: str = Depends(get_current_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    users = await user_dao.get_users()

    # 페이지네이션 로직
    total_items = len(users)
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    users = users[offset : offset + per_page]

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "users": users,
    }


@router.post(
    "/subscription/{follow_user_id}",
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def toggle_subscription(
    follow_user_id: str,
    subscribe: bool = True,
    current_user: str = Depends(get_current_session),
):
    if current_user == follow_user_id:
        raise HTTPException(status_code=400, detail="본인을 구독 할 수 없습니다.")
    try:
        await user_service.modify_subscribe_user(
            current_user, follow_user_id, subscribe
        )
        if subscribe:
            return {"message": "구독 완료"}
        else:
            return {"message": "구독 취소 완료"}
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(status_code=400, detail="이미 구독 중입니다.")
        else:
            raise


@router.get(
    "/subscription/status/{follow_user_id}",
    dependencies=[Depends(get_current_session)],
    responses=common_responses,
)
async def check_subscription_status(
    follow_user_id: str, current_user: str = Depends(get_current_session)
):
    is_subscribed = await user_service.is_user_subscribed(current_user, follow_user_id)
    return {"is_subscribed": is_subscribed}


@router.get(
    "/{user_id}/fans", response_model=PeopleResponse, responses=common_responses
)
async def get_fans(user_id: str):
    return {"people": await user_service.get_fans(user_id)}


@router.get(
    "/{user_id}/subscriptions",
    response_model=PeopleResponse,
    responses=common_responses,
)
async def get_subscriptions(user_id: str):
    return {"people": await user_service.get_subscriptions(user_id)}
