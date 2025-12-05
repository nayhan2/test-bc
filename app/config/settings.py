"""
Configuration Settings
Loads environment variables and application settings
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Supabase Configuration
    # Read from environment variables first, fallback to hardcoded values
    SUPABASE_URL: str = os.getenv(
        "SUPABASE_URL", 
        "https://lqwtfwwcbjxzvzgcjlyo.supabase.co"
    )
    SUPABASE_KEY: str = os.getenv(
        "SUPABASE_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxxd3Rmd3djYmp4enZ6Z2NqbHlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzA2MDQsImV4cCI6MjA4MDUwNjYwNH0.n7kHwIbauN_Rue0SlJhw7LGoTRbcn3CprXopW4Q6g6Q"
    )
    
    # Blockchain Configuration
    MINING_DIFFICULTY: int = int(os.getenv("MINING_DIFFICULTY", "4"))
    MINING_REWARD: float = float(os.getenv("MINING_REWARD", "10.0"))
    
    # API Configuration
    API_TITLE: str = "Blockchain API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A complete blockchain system with Supabase integration"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

