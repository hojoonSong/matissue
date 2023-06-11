import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from .config import get_settings

templates = Jinja2Templates(directory="templates")
settings = get_settings()

SMTP_SERVER = settings.smtp_server
SMTP_PORT = settings.smtp_port
SMTP_PASSWORD = settings.smtp_password
SENDER_EMAIL = settings.sender_email


def send_html_email(receiver_email, subject, template_name, template_context):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject

    html_content = templates.get_template(template_name).render(template_context)
    body = MIMEText(html_content, "html")
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
    template_name = "verification_email.html"
    template_context = {"verification_link": verification_link}
    result = send_html_email(email, subject, template_name, template_context)
    if "error" in result:
        raise HTTPException(status_code=500, detail="이메일 전송 실패")
