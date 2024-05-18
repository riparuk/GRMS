import os
from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 3306))
    DATABASE_USER: str = os.getenv("DATABASE_USER", "user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "password")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "database_name")

    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    # OpenAI API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

    # Other settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Application")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ["true", "1", "yes"]

    class Config:
        env_file = ".env"

settings = Settings()

