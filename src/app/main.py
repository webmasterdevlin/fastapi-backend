import logging
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from fastapi import FastAPI, APIRouter, Security
from fastapi.middleware.cors import CORSMiddleware

from src.app.features.users import users_routes
from src.app.features.posts import posts_router
from src.app.helpers.config import settings

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


# TODO: Fix 401 Unauthorized error in the frontend
@router.get("/", dependencies=[Security(azure_scheme, scopes=["user_impersonation"])])
async def root() -> dict[str, str]:
    log.info("Root endpoint")
    return {"message": "Hello World"}


@router.get(
    "/health", dependencies=[Security(azure_scheme, scopes=[USER_IMPERSONATION_SCOPE])]
)
async def get_health_status() -> dict[str, str]:
    url = get_url()
    return {"status": "UP", "database_connection_url": url}


@router.get("/hello/{name}")
async def say_hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}


app.include_router(router)
app.include_router(posts_router.router, prefix=prefix, tags=["posts"])
app.include_router(users_routes.router, prefix=prefix, tags=["users"])

# @app.on_event('startup')
# async def load_config() -> None:
#     """
#     Load OpenID config on startup.
#     """
#     await azure_scheme.openid_config.load_config()


# app.include_router(
#     api_router_azure_auth,
#     prefix=settings.API_V1_STR,
#     dependencies=[Security(azure_scheme, scopes=['user_impersonation'])],
# )
# app.include_router(
#     api_router_multi_auth,
#     prefix=settings.API_V1_STR,
#     # Dependencies specified on the API itself
# )
# app.include_router(
#     api_router_graph,
#     prefix=settings.API_V1_STR,
#     # Dependencies specified on the API itself
# )

# if __name__ == '__main__':
#     parser = ArgumentParser()
#     parser.add_argument('--api', action='store_true')
#     parser.add_argument('--reload', action='store_true')
#     args = parser.parse_args()
#     if args.api:
#         uvicorn.run('main:app', reload=args.reload)
#     else:
#         raise ValueError('No valid combination of arguments provided.')
