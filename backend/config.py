import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-this")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    admin_email: str = os.getenv("ADMIN_EMAIL", "salomhacker@gmail.com")
    admin_password: str = os.getenv("ADMIN_PASSWORD", "salomhacker")
    telegram_admin: str = os.getenv("TELEGRAM_ADMIN", "@begzodjon070")
    daily_request_limit: int = int(os.getenv("DAILY_REQUEST_LIMIT", "10"))

settings = Settings()
