from pydantic import Field, computed_field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Literal

# This is where sensitive and non-sensitive information is defined
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = Field(default='FastAPI backend')
    API_PREFIX: str = '/api'

    # Microsoft Entra ID settings
    OPENAPI_CLIENT_ID: str
    TENANT_ID: str
    APP_CLIENT_ID: str
    AUTH_URL: str
    CONFIG_URL: str
    TOKEN_URL: str = 2
    GRAPH_SECRET: str
    CLIENT_SECRET: str

    # Postgres settings
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
