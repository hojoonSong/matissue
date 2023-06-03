import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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


# # 이메일 보내기
# receiver_email = "bmp.tom@yahoo.com"
# subject = "Test Email"
# message = "This is a test email from Python."

# result = send_email(receiver_email, subject, message)
# if "error" in result:
#     print(result["error"])
# else:
#     print(result["status"])
