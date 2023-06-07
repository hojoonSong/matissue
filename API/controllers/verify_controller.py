from fastapi import Query, Depends, HTTPException, APIRouter
from utils.session_manager import SessionManager
from models.user_models import UserForgotIDIn, UserForgotPasswordIn
from services.user_service import UserService
from dao.user_dao import UserDao, get_user_dao
from datetime import datetime
from utils.email_manager import send_email

router = APIRouter()
session_manager = SessionManager()


@router.get("/verify", status_code=200)
async def verify(code: str = Query(...), session_manager: SessionManager = Depends(SessionManager), user_dao: UserDao = Depends(get_user_dao)):
    email = session_manager.verify_email(code)
    if not email:
        raise HTTPException(status_code=400, detail="유효하지 않은 주소입니다.")

    # 이메일 인증이 완료되면, 캐싱해뒀던 사용자 정보를 불러와서 회원가입 진행
    user_in = session_manager.get_user_info(email)
    if user_in is None:
        raise HTTPException(
            status_code=400, detail="이메일 인증 코드가 만료되었거나 잘못되었습니다.")

    user_service = UserService(user_dao)
    created_user = await user_service.create_user(user_in)
    if not created_user:
        raise HTTPException(status_code=400, detail="계정을 생성할 수 없습니다.")

    return {"user_id": user_in.user_id,
            "username": user_in.username,
            "email": user_in.email,
            "birth_date": user_in.birth_date,
            "img": user_in.img,
            "created_at": datetime.now()}


@router.post("/forgot-id", status_code=200)
async def forgot_id(user: UserForgotIDIn, user_dao: UserDao = Depends(get_user_dao)):
    existing_user = await user_dao.get_user_by_email_and_birthdate(user.email, user.birth_date)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail="해당 정보를 가진 사용자를 찾을 수 없습니다.")

    subject = "맛이슈, 아이디 찾기 요청입니다."
    message = f"귀하의 아이디는 {existing_user.user_id} 입니다."

    result = send_email(user.email, subject, message)
    if "error" in result:
        raise HTTPException(status_code=500, detail="이메일 전송 실패")

    return {"message": "아이디가 이메일로 발송되었습니다. 이메일을 확인해 주세요."}


@router.post("/forgot-password", status_code=200)
async def forgot_password(user: UserForgotPasswordIn, user_dao: UserDao = Depends(get_user_dao), session_manager: SessionManager = Depends(SessionManager)):
    existing_user = await user_dao.get_user_by_id_and_birthdate(user.user_id, user.birth_date)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail="해당 정보를 가진 사용자를 찾을 수 없습니다.")

    temporary_password = session_manager.create_temporary_password(
        user.user_id)
    subject = "맛이슈, 임시 비밀번호 발송"
    message = f"귀하의 임시 비밀번호는 {temporary_password} 입니다. 로그인 후 반드시 비밀번호를 변경해주세요."

    result = send_email(existing_user.email, subject, message)
    if "error" in result:
        raise HTTPException(status_code=500, detail="이메일 전송 실패")

    return {"message": "임시 비밀번호가 이메일로 발송되었습니다. 이메일을 확인해 주세요."}
