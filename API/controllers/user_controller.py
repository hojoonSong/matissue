from services.user_service import UserService
from dao.user_dao import UserDao
from models.user_models import UserUpdate, UserIn, UserOut, UserInDB
from models.response_models import LoginResponse, LoginRequest, MessageResponse, FollowsResponse
from fastapi import APIRouter, HTTPException, Response, Depends, Query, Request
from typing import List
from utils.session_manager import SessionManager, get_current_session, get_current_user
from utils.permission_manager import check_user_permissions
from utils.response_manager import common_responses
from utils.email_manager import send_email

router = APIRouter()
user_dao = UserDao()
user_service = UserService(user_dao)



@router.post("/", status_code=201, responses=common_responses)
async def create_user(user: UserIn, session_manager: SessionManager = Depends(SessionManager)):
    existing_user = await user_dao.get_user_by_id(user.user_id)
    if existing_user:
            raise HTTPException(
    status_code=404, detail=f"사용자 아이디 '{user.user_id}'은 사용할 수 없습니다.")

    exiting_email = await user_dao.get_user_by_email(user.email)
    if exiting_email:
        raise HTTPException(
    status_code=404, detail=f"사용자 이메일 '{user.email}'은 사용할 수 없습니다.")


    verification_code = session_manager.create_verification_code(user.email)
    verification_link = f"https://localhost:8000/api/verify?code={verification_code}"

    subject = "맛이슈 가입인증 이메일입니다."
    message = f"가입 인증을 완료하려면 다음 링크를 클릭하세요: {verification_link}"
    "이 이메일 인증 코드는 24시간 동안만 유효합니다."

    result = send_email(user.email, subject, message)
    if "error" in result:
        raise HTTPException(status_code=500, detail="이메일 전송 실패")

    session_manager.save_user_info(user)

    return {"message": "인증 이메일이 발송되었습니다. 이메일을 확인해 주세요."}


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
async def delete_user(user: LoginRequest, request: Request, current_user: str = Depends(get_current_session)):
    session_id = request.cookies.get("session-id")
    check_user_permissions(user.user_id, current_user)
    result = await user_service.delete_user(user.user_id, user.password, str(session_id))
    if not result:
        raise HTTPException(status_code=400, detail="사용자 탈퇴에 실패하였습니다.")

    return MessageResponse(message="성공적으로 탈퇴되었습니다!")


@router.post("/login", response_model=LoginResponse, responses=common_responses)
async def login(user: LoginRequest, response: Response):
    result = await user_service.login(user.user_id, user.password)
    if result:
        response.set_cookie(
            key="session-id", value=result["session_id"], secure="None", httponly="True", samesite="None")
        return LoginResponse(message="로그인에 성공했습니다!", session_id=result["session_id"])
    raise HTTPException(status_code=400, detail="로그인에 실패했습니다.")


@router.post("/logout", response_model=MessageResponse, dependencies=[Depends(get_current_session)], responses=common_responses)
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session-id")
    result = await user_service.logout(session_id, response)
    if result['detail'] == '성공적으로 로그아웃되었습니다.':
        return MessageResponse(message=result["detail"])
    raise HTTPException(status_code=400, detail="로그아웃에 실패했습니다.")


@router.get("/me", response_model=UserOut, dependencies=[Depends(get_current_session)], responses=common_responses)
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
        "created_at": user_in_db.created_at
    }


@router.get("/", dependencies=[Depends(get_current_session)], responses=common_responses)
async def get_users(
    current_user: str = Depends(get_current_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1)
):
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    users = await user_dao.get_users()

    # 페이지네이션 로직
    total_items = len(users)
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    users = users[offset:offset + per_page]

    return {
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "total_items": total_items,
        "users": users
    }

@router.post("/subscription/{follow_user_id}", dependencies=[Depends(get_current_session)], responses=common_responses)
async def toggle_subscription(follow_user_id: str, subscribe: bool = True, current_user: str = Depends(get_current_session)):
    if current_user == follow_user_id:
        raise HTTPException(status_code=400, detail="본인을 구독 할 수 없습니다.")
    try:
        await user_service.modify_subscribe_user(current_user, follow_user_id, subscribe)
        if subscribe:
            return {"message": "구독 완료"}
        else:
            return {"message": "구독 취소 완료"}
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(status_code=400, detail="이미 구독 중입니다.")
        else:
            raise

@router.get("/{user_id}/followers", response_model=List[FollowsResponse], responses=common_responses)
async def get_followers(user_id: str):
    return await user_service.get_followers(user_id)


