from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENVIRONMENT_FILE_PATH = Path(__file__).parent.parent / ".env"

if not ENVIRONMENT_FILE_PATH.exists():
    raise FileNotFoundError(f"The environment file does not exist: {ENVIRONMENT_FILE_PATH}")

class Config(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file=str(ENVIRONMENT_FILE_PATH), extra="ignore")

env = Config()  # type: ignore


            
        