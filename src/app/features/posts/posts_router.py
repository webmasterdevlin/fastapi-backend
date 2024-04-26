from typing import Any
from fastapi import APIRouter
from sqlmodel import select, func

from src.app.helpers.dependencies import SessionDep
from src.app.helpers.models import Post, PostsPublic


router = APIRouter()


@router.get("/", response_model=PostsPublic)
def read_posts(
    session: SessionDep, author_id: int, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve posts.
    """
    count_statement = (
        select(func.count()).select_from(Post).where(Post.author_id == author_id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Post).where(Post.author_id == author_id).offset(skip).limit(limit)
    )
    posts = session.exec(statement).all()
    return PostsPublic(data=posts, count=count)
