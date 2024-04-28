from typing import Any
from sqlalchemy import Null
from sqlmodel import select, func

from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostCreate, PostsPublic


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


def create_new_post(*, session: SessionDep, post: PostCreate, author_id: int) -> Post:
    db_post = Post.model_validate(post, update={"author_id": author_id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


def update_post(*, session: SessionDep, post: Post, updated_post: Post) -> Post:
    update_dict = updated_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_dict)
    session.commit()
    session.refresh(post)
    return post


def delete_post(*, session: SessionDep, post: Post) -> None:
    session.delete(post)
    session.commit()
