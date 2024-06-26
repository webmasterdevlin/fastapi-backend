from typing import Dict, Union

from src.app.helpers.dependencies import validate_is_admin_user
from src.app.features.greetings.models import HelloWorldResponse
from fastapi import APIRouter, Depends, Request

from fastapi_azure_auth.user import User

router = APIRouter()


@router.get(
    '/hello',
    response_model=HelloWorldResponse,
    summary='Say hello',
    name='hello_world',
    operation_id='helloWorld',
    dependencies=[Depends(validate_is_admin_user)],
)
async def world(request: Request) -> Dict[str, Union[str, User]]:
    """
    Wonder who we say hello to?
    """
    user: User = request.state.user
    return {'hello': 'world', 'user': user}
