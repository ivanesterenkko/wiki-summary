from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class AppSettings(BaseSetting):
    BASE_DIR: Path = BASE_DIR
    SERVICE_NAME: str
    SERVICE_VERSION: str
    API_VERSION: str
    ENVIRONMENT: str
    SERVICE_PORT: int = 8080
    SECRET_KEY: str
    ALGORITHM: str


class OpenAiSettings(BaseSetting):
    OPENAI_SECRET_KEY: str
    OPENAI_URL: str


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POOL_SIZE: int = 40
    POOL_MAX_OVERFLOW: int = 10
    SQL_ECHO: bool = True

    @property
    def db_uri(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


app_settings = AppSettings()
openai_settings = OpenAiSettings()
db_settings = DBSettings()
