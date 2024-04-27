from typing import Any

from fastapi import APIRouter
from sqlmodel import select, func

from .services import create_new_post
from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostsPublic

router = APIRouter()


@router.get("/posts", response_model=PostsPublic)
def read_posts(
    session: SessionDep, author_id: int, skip: int = 0, limit: int = 10
) -> PostsPublic:
    """
    Retrieve posts with query parameters author_id, skip, and limit.
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


@router.get("/posts/{post_id}", response_model=Post)
def read_post_by_id(session: SessionDep, post_id: int) -> Any:
    """
    Retrieve a post by id using a url parameter post_id.
    """
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    return post


@router.post("/posts", response_model=Post, tags=["posts"])
def create_post(session: SessionDep, post: Post, author_id: int) -> Any:
    """
    Create a post.
    """
    return create_new_post(
        session=session,
        post=post,
        author_id=author_id,  # type: ignore
    )


# 4. Add a route to update a post
@router.put("/posts/{post_id}", response_model=Post)
def update_post(session: SessionDep, post_id: int, post_in: Post) -> Any:
    """
    Update a post using a url parameter post_id and a request body post_in.
    """
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    post = post_in
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# 5. Add a route to delete a post
@router.delete("/posts/{post_id}", response_model=None)
def delete_post(session: SessionDep, post_id: int) -> None:
    """
    Delete a post.
    """
    post = session.exec(select(Post).where(Post.id == post_id)).first()
    session.delete(post)
    session.commit()
