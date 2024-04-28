from .services import get_user_by_id, remove_user_by_id, update_user, create_new_user

from typing import Any

from fastapi import APIRouter

from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import User

router = APIRouter()


@router.get("/users/{user_id}", response_model=User, tags=["users"])
def read_user_by_id(session: SessionDep, user_id: int) -> Any:
    """
    Retrieve a user by their ID.

    Args:
        session (SessionDep): The database session dependency.
        user_id (int): The ID of the user to retrieve.

    Returns:
        Any: The user object.

    """
    return get_user_by_id(session=session, user_id=user_id)


@router.post("/users", response_model=User, tags=["users"])
def create_user(session: SessionDep, user: User) -> Any:
    """
    Create a new user.

    Args:
        session (SessionDep): The database session.
        user (User): The user data.

    Returns:
        Any: The created user.

    """
    return create_new_user(session=session, user=user)


@router.put("/users/{user_id}", response_model=User, tags=["users"])
def put_user(session: SessionDep, user_id: int, user: User) -> Any:
    """
    Update a user with the specified user_id.

    Args:
        session (SessionDep): The database session.
        user_id (int): The ID of the user to update.
        user (User): The updated user object.

    Returns:
        Any: The updated user object.

    """
    return update_user(session=session, user_id=user_id, updated_user=user)


@router.delete("/users/{user_id}", tags=["users"])
def delete_user(session: SessionDep, user_id: int) -> Any:
    """
    Delete a user by their ID.

    Args:
        session (SessionDep): The database session.
        user_id (int): The ID of the user to delete.

    Returns:
        Any: The result of removing the user.
    """
    return remove_user_by_id(session=session, user_id=user_id)
