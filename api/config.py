from pydantic import Field, computed_field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

# This is where sensitive and non-sensitive information is defined
class Settings(BaseSettings):
    # General settings not in secrets manager
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = Field(default='FastAPI backend')
    API_PREFIX: str = '/api'
    POSTGRES_PORT: int = 5432

    # Non-sensitive Microsoft Entra ID settings
    AUTH_URL: str = "https://login.microsoftonline.com/"
    CONFIG_URL: str = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
    TOKEN_URL: str = "https://login.microsoftonline.com/common/oauth2/v2.0/token"

    # Sensitive Microsoft Entra ID settings
    OPENAPI_CLIENT_ID: str
    TENANT_ID: str
    APP_CLIENT_ID: str
    GRAPH_SECRET: str
    CLIENT_SECRET: str

    # Postgres settings
    POSTGRES_SERVER: str
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
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()  # type: ignore
