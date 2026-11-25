from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Shop API"
    app_debug: bool = True
    app_secret_key: str = "super_secret_key_change_me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite+aiosqlite:///./shop.db"
    upload_dir: str = "uploads"
    max_upload_size: int = 5 * 1024 * 1024  # 5 MB

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()