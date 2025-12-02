# backend/app/core/config.py
from typing import Optional
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Get the backend directory path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ENV_FILE = os.path.join(BACKEND_DIR, ".env")

# Load environment variables
load_dotenv(ENV_FILE)

class Settings(BaseSettings):
    GEMINI_API_KEY: Optional[str] = None
    
    # Database Config
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "username")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "yourpassword")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "yourhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "portnumber"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "dbname")

    # Data Paths (Default to local folders if not set in .env)
    # You can now change these in .env to point anywhere on your disk
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_store")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./storage")

    class Config:
        env_file = ENV_FILE
        extra = "ignore"

# Create settings instance
settings = Settings()

# --- AUTO-CREATE DIRECTORIES ---
# This ensures that if you change the path in .env, the new folders 
# are created automatically without errors.
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PATH, exist_ok=True)