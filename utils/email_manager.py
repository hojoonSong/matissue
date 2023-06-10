import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from .config import get_settings

settings = get_settings()

SMTP_SERVER = settings.smtp_server
SMTP_PORT = settings.smtp_port
SMTP_PASSWORD = settings.smtp_password
SENDER_EMAIL = settings.sender_email


def send_email(receiver_email, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject

    body = MIMEText(message, "plain")
    msg.attach(body)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
            return {"status": "Email sent successfully"}
    except smtplib.SMTPException as e:
        error_message = str(e)
        return {"error": f"Failed to send email: {error_message}"}


def send_verification_email(email: str, verification_link: str) -> None:
    subject = "맛이슈 가입인증 이메일입니다."
    message = f"가입 인증을 완료하려면 다음 링크를 클릭하세요: {verification_link} 이 이메일 인증 코드는 24시간 동안만 유효합니다."
    result = send_email(email, subject, message)
    if "error" in result:
        raise HTTPException(status_code=500, detail="이메일 전송 실패")
