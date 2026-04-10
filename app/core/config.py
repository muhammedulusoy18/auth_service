import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "yedek_gizli_anahtar")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    AUTHDATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./auth_app.db")
    EVENTDB_URL: str = os.getenv("EVENTDB_URL", "sqlite:///./eventdb.db")
    PASSWORD_EXPIRE_TOKEN:int=int(os.getenv("PASSWORD_REFRESH_TOKEN_EXPİRE_MINUTES"))
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD" )
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_FROM = os.getenv("MAIL_FROM")
    admin_role: str=  "admin"
    editor_role: str="editor"
    user_role: str="user"
settings = Settings()