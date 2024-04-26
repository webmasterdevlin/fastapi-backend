from typing import Any
from fastapi import APIRouter
from sqlmodel import select, func

from src.app.features.users.services import create_new_user
from src.app.helpers.dependencies import SessionDep
from src.app.helpers.models import User, UserCreate, UsersPublic


router = APIRouter()


# 1. Add a route to retrieve users
@router.get("/users", response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 10) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return UsersPublic(data=users, count=count)  # type: ignore


# 2. Add a route to retrieve a user by id
@router.get("/users/{user_id}", response_model=User)
def read_user_by_id(session: SessionDep, user_id: int) -> Any:
    """
    Retrieve a user by id.
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


# 3. Add a route to retrieve a user by email
@router.get("/users/email/{email}", response_model=User)
def read_user_by_email(session: SessionDep, email: str) -> Any:
    """
    Retrieve a user by email.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


# 4. Add a route to create a user
@router.post("/users", response_model=User)
def create_user(session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create a user.
    """
    user = create_new_user(session=session, user_create=user_in)
    return user
