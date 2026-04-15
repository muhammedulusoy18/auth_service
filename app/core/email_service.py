import smtplib,qrcode,io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
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
def send_ticket_confirmation_mail(email_to:str,ticket_data:dict):
    qr_content=(f"TicketID:{ticket_data['ticket_id']} \n"
                f"Event Name:{ticket_data['event_name']}\n"
                f"Quantity:{ticket_data['quantity']}\n"
                f"Date:{ticket_data['purchase_date']}\n"
                f"VERIFICATION-CODE: {ticket_data.get('ticket_uuid')}\n"
                )
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_data = buffered.read()
    qr_image = MIMEImage(img_data)
    qr_image.add_header('Content-ID', '<qr_code>')
    msg = MIMEMultipart()
    msg["From"] = settings.MAIL_FROM
    msg["To"] = email_to
    msg["Subject"]=f"biletiniz onaylandı 🎫 -{ticket_data['event_name']}"
    html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #ffffff; border: 1px solid #ddd; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #4CAF50; text-align: center; margin-bottom: 10px;">Biletiniz Onaylandı! 🎫</h2>
                    <p style="text-align: center; color: #666;">Keyifli eğlenceler dileriz.</p>
                    <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">

                    <p>Merhaba,</p>
                    <p><b>{ticket_data['event_name']}</b> etkinliği için biletiniz başarıyla oluşturuldu. Bilet detaylarınız aşağıdadır:</p>

                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #4CAF50;">
                        <p style="margin: 5px 0;"><b>Etkinlik:</b> {ticket_data['event_name']}</p>
                        <p style="margin: 5px 0;"><b>Bilet No:</b> #{ticket_data['ticket_id']}</p>
                        <p style="margin: 5px 0;"><b>Adet:</b> {ticket_data['quantity']} Kişilik</p>
                        <p style="margin: 5px 0;"><b>İşlem Tarihi:</b> {ticket_data['purchase_date']}</p>
                    </div>

                    <div style="text-align: center; margin: 30px 0; padding: 20px; border: 2px dashed #ddd; border-radius: 10px;">
                        <p style="margin-bottom: 15px; font-weight: bold; color: #444;">Giriş İçin QR Kodunuzu Okutun</p>

                        <img src="cid:qr_code" alt="Bilet QR Kodu" style="width: 200px; height: 200px;"/>

                        <p style="margin-top: 10px; font-size: 11px; color: #999;">Doğrulama Kodu: {ticket_data.get('ticket_uuid', 'N/A')}</p>
                    </div>

                    <p style="text-align: center; color: #888; font-size: 12px; margin-top: 30px;">
                        Bu bilet dijital olarak üretilmiştir. Giriş esnasında QR kodu görevliye göstermeniz yeterlidir.
                    </p>
                </div>
            </body>
        </html>
        """
    msg.attach(MIMEText(html, "html"))
    msg.attach(MIMEText(html, "html"))
    msg.attach(qr_image)
    with smtplib.SMTP(settings.MAIL_SERVER,settings.MAIL_PORT) as server:
        server.starttls()
        server.login(settings.MAIL_FROM,settings.MAIL_PASSWORD)
        server.sendmail(settings.MAIL_FROM,email_to,msg.as_string())
