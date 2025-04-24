import os
from pydantic import PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "DocAI"
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "maindb")
    
    DATABASE_URL: PostgresDsn = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "9768a4f349e9c0cb3a3b3c16fb54b87c")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

settings = Settings()