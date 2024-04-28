from fastapi.responses import JSONResponse
from .services import get_user_by_id, update_user, create_new_user

from typing import Any

from fastapi import APIRouter

from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import User

router = APIRouter()


@router.get("/users/{user_id}", response_model=User, tags=["users"])
def read_user_by_id(session: SessionDep, user_id: int) -> Any:
    """
    Retrieve a user by id using a url parameter user_id.
    """
    user = get_user_by_id(session=session, user_id=user_id)
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    else:
        return user


@router.post("/users", response_model=User, tags=["users"])
def create_user(session: SessionDep, user: User) -> Any:
    """
    Create a user using a request body user.
    """
    return create_new_user(session=session, user=user)


@router.put("/users/{user_id}", response_model=User, tags=["users"])
def put_user(session: SessionDep, user_id: int, user: User) -> Any:
    """
    Update a user.
    """
    return update_user(session=session, user_id=user_id, updated_user=user)


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(session: SessionDep, user_id: int) -> Any:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    else:
        session.delete(user)
        session.commit()
        return JSONResponse(status_code=204, content={"message": "User deleted"})
