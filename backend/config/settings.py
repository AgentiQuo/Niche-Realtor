import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from the root of the project
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # AI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENROUTER_BASE_URL: str = os.getenv("ANTHROPIC_BASE_URL", "https://openrouter.ai/api/v1")
    DEFAULT_MODEL: str = os.getenv("ANTHROPIC_MODEL", "nvidia/nemotron-3-super")
    
    # App Settings
    PROJECT_NAME: str = "Niche Realtor"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
