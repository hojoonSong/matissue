from fastapi import HTTPException


def check_user_permissions(user_id: str, current_user: str):
    if current_user != user_id and current_user != "admin":
        raise HTTPException(status_code=401, detail="Invalid session ID")

    if current_user != user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
