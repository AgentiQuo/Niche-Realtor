import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # AI Configuration (OpenAI as default fallback if used)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # App Settings
    PROJECT_NAME: str = "Niche Realtor"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
