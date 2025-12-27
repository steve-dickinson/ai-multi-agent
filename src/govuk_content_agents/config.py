from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration using Pydantic Settings.
    Reads from environment variables and .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    APP_NAME: str = "GOV.UK Content Agents"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # APIs
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="API key for Google Gemini")
    OPENAI_API_KEY: str = Field(..., description="API key for OpenAI")
    
    # Database - MongoDB
    MONGO_URI: str = Field(default="mongodb://admin:password@localhost:27018", description="MongoDB connection URI")
    MONGO_DB_NAME: str = Field(default="govuk_agents", description="MongoDB database name")
    
    # Database - PostgreSQL (pgvector)
    POSTGRES_USER: str = Field(default="admin")
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_DB: str = Field(default="ai_agent_db")
    
    @property
    def POSTGRES_URI(self) -> str:
        """Construct PostgreSQL URI from components."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
