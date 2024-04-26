from typing import Any
from fastapi import APIRouter
from sqlmodel import select, func

from src.app.helpers.dependencies import SessionDep
from src.app.helpers.models import User, UsersPublic


router = APIRouter()


@router.get("/", response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 10) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return UsersPublic(data=users, count=count)
