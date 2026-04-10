import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.config import settings


def send_reset_password_email(email_to:str,token:str):
    msg = MIMEMultipart()
    msg["From"] = settings.MAIL_FROM
    msg["To"] = email_to
    msg["Subject"] = "Şifre sıfırlama isteği 🔒 "
    link=f"http://localhost:8000/auth/resetpassword?token={token}"
    html=f"""
    <html>
        <body>
            <p>Merhaba,<p>
            <p>Şifrenizi sıfırlamak için aşağıdaki butona tıklayın:</p>
            <a href="{link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none;">Şifremi Sıfırla</a>
            <p>Bu link 15 dakika geçerlidir.</p>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))
    with  smtplib.SMTP(settings.MAIL_SERVER,settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_FROM,settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM,email_to,msg.as_string())