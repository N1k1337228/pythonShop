from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Shop API"
    app_debug: bool = True
    app_secret_key: str = "change_me"
    database_url: str = "sqlite+aiosqlite:///./shop.db"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    upload_dir: str = "uploads"
    max_upload_size: int = 5 * 1024 * 1024

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()