from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    postgres_url: str = "postgresql://ekaterinariadcikova:password@localhost:5432/tickets_db"
    
    # Security
    secret_key: str = "secret123"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Tickets Booking API"
    
    # CORS
    backend_cors_origins: list = [
        "http://localhost:3000", 
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://localhost:44445",
        "http://127.0.0.1:44445"
    ]
    
    class Config:
        env_file = ".env"


settings = Settings()
