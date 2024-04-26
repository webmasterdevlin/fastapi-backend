from typing import Any
from fastapi import APIRouter
from sqlmodel import select, func

from src.app.helpers.dependencies import SessionDep
from src.app.helpers.models import Post, PostCreate, PostsPublic


router = APIRouter()


# 1. Add a route to retrieve posts
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
    return PostsPublic(data=posts, count=count)  # type: ignore


# 2. Add a route to retrieve a post by id
@router.get("/{post_id}", response_model=Post)
def read_post_by_id(session: SessionDep, post_id: int) -> Any:
    """
    Retrieve a post by id.
    """
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    return post


# 3. Add a route to create a post
@router.post("/", response_model=Post)
def create_post(session: SessionDep, post_in: PostCreate, author_id: int) -> Any:
    """
    Create a post.
    """
    post = create_post(session=session, post_in=post_in, author_id=author_id)
    return post
