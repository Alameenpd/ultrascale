from pydantic import BaseSettings
import logging

class Settings(BaseSettings):
    # Database configuration
    database_url: str = "postgresql://user:password@localhost:5432/ultrascale"
    
    # Security settings
    secret_key: str = "your_secret_key"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # Redis configuration for Celery and rate limiting
    redis_url: str = "redis://localhost:6379/0"

    # Logging configuration
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

# Initialize settings
settings = Settings()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("ultrascale-backend")
