from pydantic import Field, computed_field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Literal

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

# This is where sensitive and non-sensitive information is defined
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = Field(default='FastAPI backend')
    API_PREFIX: str = '/api'
    DOMAIN: str = "http://localhost"

    # Microsoft Entra ID settings
    OPENAPI_CLIENT_ID: str
    TENANT_ID: str
    APP_CLIENT_ID: str
    AUTH_URL: str
    CONFIG_URL: str
    TOKEN_URL: str
    GRAPH_SECRET: str
    CLIENT_SECRET: str

    # Postgres settings
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
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
