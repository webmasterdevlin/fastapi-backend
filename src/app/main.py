import logging
from pydantic import BaseModel, Field
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
from fastapi import FastAPI, APIRouter, Security
from fastapi.middleware.cors import CORSMiddleware

from .features.users import users_routes
from .features.posts import posts_routes
from .helpers.config import settings

log = logging.getLogger(__name__)

USER_IMPERSONATION_SCOPE = "user_impersonation"


def get_url() -> str:
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    server = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    db = settings.POSTGRES_DB
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"


app = FastAPI(
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": settings.OPENAPI_CLIENT_ID,
        "scopes": settings.SCOPE_NAME,
    },
    version="1.0.0",
    description="## Welcome to my API! \n This is my description, written in `markdown`",
    title=settings.PROJECT_NAME,
)

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    tenant_id=settings.TENANT_ID,
    scopes=settings.SCOPES,
)

# Define a list of origins that should be permitted to make cross-origin requests
origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
prefix = settings.API_PREFIX

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # type: ignore
    allow_credentials=True,  # type: ignore
    allow_methods=["*"],  # type: ignore
    allow_headers=["*"],  # type: ignore
)


class User(BaseModel):
    email: str
    password: str
    is_active: bool = Field(..., alias="isActive")

    class Config:
        allow_population_by_field_name = True


class UserDTO(BaseModel):
    email: str


router = APIRouter(
    prefix=prefix,
)


@router.on_event("startup")  # type: ignore
async def load_config() -> None:
    print("Loading OpenID config on startup")
    await azure_scheme.openid_config.load_config()


@router.on_event("shutdown")  # type: ignore
async def shutdown_event() -> None:
    print("Application shutdown")


@router.get(
    "/health", dependencies=[Security(azure_scheme, scopes=[USER_IMPERSONATION_SCOPE])]
)
def get_health_status() -> dict[str, str]:
    url = get_url()
    return {"status": "UP", "database_connection_url": url}


@router.get("/hello/{name}")
def say_hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}


@router.post("/dto")
def make_user(user: User):
    user_dict = user.model_dump()
    new_user = UserDTO(**user_dict)
    return new_user


app.include_router(router)
app.include_router(posts_routes.router, prefix=prefix, tags=["posts"])
app.include_router(users_routes.router, prefix=prefix, tags=["users"])
