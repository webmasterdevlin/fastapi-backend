import logging
from argparse import ArgumentParser

import uvicorn
from api.api_v1.api import api_router_azure_auth, api_router_graph, api_router_multi_auth
from api.dependencies import azure_scheme
from core.config import settings
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger(__name__)

app = FastAPI(
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': settings.OPENAPI_CLIENT_ID,
        'additionalQueryStringParams': {'prompt': 'consent'},
    },
    version='1.0.0',
    description='## Welcome to my API! \n This is my description, written in `markdown`',
    title=settings.PROJECT_NAME,
)

# Define a list of origins that should be permitted to make cross-origin requests
origins = [
    "http://localhost:3000",  # React app's origin in development
    "http://localhost:8080",  # React app's origin in development
    "https://lemon-sea-0d997b303.5.azurestaticapps.net",  # React app's production domain
]

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:  # pragma: no cover
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],  # type: ignore
        allow_credentials=True,  # type: ignore
        allow_methods=['*'],  # type: ignore
        allow_headers=['*'],  # type: ignore
    )




@app.get("/api/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


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
