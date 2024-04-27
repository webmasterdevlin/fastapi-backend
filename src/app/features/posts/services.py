# complete crud for post
from fastapi import HTTPException
from sqlmodel import Session, select

from src.app.schemas.models import Post, PostCreate


# creating a post
def create_new_post(*, session: Session, post: PostCreate, author_id: int) -> Post:
    db_post = Post.model_validate(post, update={"author_id": author_id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# updating a post
def update_post(*, session: Session, id: int, updated_post: Post) -> Post:
    updated_post = session.get(Post, id)  # type: ignore
    if not updated_post:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = updated_post.model_dump(exclude_unset=True)
    updated_post.sqlmodel_update(update_dict)
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return updated_post


# getting a post by id
def get_post_by_id(*, session: Session, post_id: int) -> Post | None:
    statement = select(Post).where(Post.id == post_id)
    session_post = session.exec(statement).first()
    return session_post


# getting all posts
def get_all_posts(*, session: Session) -> list[Post]:
    statement = select(Post)
    session_posts = session.exec(statement).all()
    return list(session_posts)


# deleting a post
def delete_post(*, session: Session, post: Post) -> None:
    session.delete(post)
    session.commit()
