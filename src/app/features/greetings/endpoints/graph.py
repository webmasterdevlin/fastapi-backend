from typing import Any

import httpx
from src.app.helpers.dependencies import azure_scheme
from src.app.helpers.config import settings
from fastapi import APIRouter, Depends, Request
from httpx import AsyncClient
from jose import jwt

router = APIRouter()


@router.get(
    '/hello-graph',
    summary='Fetch graph API using OBO',
    name='graph',
    operation_id='helloGraph',
    dependencies=[Depends(azure_scheme)],
)
async def graph_world(request: Request) -> Any:  # noqa: ANN401
    """
    :param request: The request object containing information about the HTTP request.
    :return: A dictionary containing the user claims obtained from the access token, the OBO response, and the graph response.

    This method fetches the graph API using On-Behalf-Of (OBO) authentication. The user's access token is used to obtain a new access token for the Graph API. The method then calls the `/me` endpoint of the Graph API to fetch more information about the current user. The obtained information is returned as a dictionary to the end user.

    Example usage:

    ```
    response = await graph_world(request)
    print(response)
    ```
    """
    async with AsyncClient() as client:
        # Use the users access token and fetch a new access token for the Graph API
        obo_response: httpx.Response = await client.post(
            f'https://login.microsoftonline.com/{settings.TENANT_ID}/oauth2/v2.0/token',
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'client_id': settings.APP_CLIENT_ID,
                'client_secret': settings.GRAPH_SECRET,
                'assertion': request.state.user.access_token,
                'scope': 'https://graph.microsoft.com/user.read',
                'requested_token_use': 'on_behalf_of',
            },
        )

        if obo_response.is_success:
            # Call the graph `/me` endpoint to fetch more information about the current user, using the new token
            graph_response: httpx.Response = await client.get(
                'https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f'Bearer {obo_response.json()["access_token"]}'},
            )
            graph = graph_response.json()
        else:
            graph = 'skipped'

        # Return all the information to the end user
        return (
            {'claims': jwt.get_unverified_claims(token=request.state.user.access_token)}
            | {'obo_response': obo_response.json()}
            | {'graph_response': graph}
        )
