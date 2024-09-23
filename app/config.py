from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """App settings."""

    project_name: str = "rinha"
    debug: bool = False
    environment: str = "dev"

    # Database
    # DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

settings = Settings()