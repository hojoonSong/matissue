from fastapi import Query, Depends, HTTPException, APIRouter
from utils.session_manager import SessionManager

router = APIRouter()


@router.get("/verify", status_code=200)
async def verify(code: str = Query(...), session_manager: SessionManager = Depends(SessionManager)):
    verification_result = session_manager.verify_email(code)
    if not verification_result:
        raise HTTPException(
            status_code=400, detail="이메일 인증 코드가 만료되었거나 잘못되었습니다.")
    else:
        return {"message": "이메일을 성공적으로 전송했습니다."}
