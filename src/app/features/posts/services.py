from typing import Any
from fastapi import HTTPException
from sqlalchemy import Null
from sqlmodel import select, func

from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostCreate, PostsPublic


def create_new_post(*, session: SessionDep, post: PostCreate, author_id: int) -> Post:
    db_post = Post.model_validate(post, update={"author_id": author_id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def update_post(*, session: SessionDep, id: int, updated_post: Post) -> Post:
    updated_post = session.get(Post, id)  # type: ignore
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")

    update_dict = updated_post.model_dump(exclude_unset=True)
    updated_post.sqlmodel_update(update_dict)
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return updated_post


def get_post_by_id(*, session: SessionDep, post_id: int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    return session.exec(statement).first()


def get_all_posts(
    *, session: SessionDep, author_id: int, skip: int = 0, limit: int = 10
) -> Any:
    count_statement = (
        select(func.count()).select_from(Post).where(Post.author_id == author_id)
    )
    count = session.exec(count_statement).first()
    if count == 0:
        return Null
    statement = (
        select(Post).where(Post.author_id == author_id).offset(skip).limit(limit)
    )
    posts = session.exec(statement).all()
    return PostsPublic(data=posts, count=count)  # type: ignore


def delete_post(*, session: SessionDep, post: Post) -> None:
    session.delete(post)
    session.commit()
