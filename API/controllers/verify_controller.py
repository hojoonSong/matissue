from fastapi import Query, Depends, HTTPException, APIRouter
from utils.session_manager import SessionManager
from services.user_service import UserService
from models.user_models import UserIn
from dao.user_dao import UserDao, get_user_dao
from datetime import datetime

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
