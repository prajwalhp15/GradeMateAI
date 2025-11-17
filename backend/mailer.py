import smtplib
from email.message import EmailMessage
from .config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD

def send_email(to_email: str, subject: str, content: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP credentials not configured. Skipping email.")
        return False
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(content)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASSWORD)
            s.send_message(msg)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False
