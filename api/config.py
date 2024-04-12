from pydantic import AnyHttpUrl, Field, computed_field, PostgresDsn
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
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = [
    "http://localhost:3000",  # React app's origin in development
    "http://localhost:8080",  # React app's origin in development
    "https://lemon-sea-0d997b303.5.azurestaticapps.net",  # React app's production domain
]

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
    SCOPE_DESCRIPTION: str = "user_impersonation"

    @computed_field
    @property
    def SCOPE_NAME(self) -> str:
        scope_name = f'api://{self.APP_CLIENT_ID}/{self.SCOPE_DESCRIPTION}'
        print(scope_name)
        return scope_name


    @computed_field
    @property
    def SCOPES(self) -> dict[str, str]:
        return {
            self.SCOPE_NAME: self.SCOPE_DESCRIPTION,
        }
    

    @computed_field
    @property
    def OPENAPI_AUTHORIZATION_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/authorize"


    @computed_field
    @property
    def OPENAPI_TOKEN_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/token"

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
