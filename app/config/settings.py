from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Configuration
    api_version: str
    api_prefix: str
    debug: bool

    # Database Configuration
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # Vector Database Configuration
    vector_db_host: str
    vector_db_port: int

    # Security
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    # Additional Database Settings
    postgres_host: str
    postgres_port: int

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
