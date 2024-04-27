# complete crud for post
from sqlmodel import Session, select

from src.app.schemas.models import Post


# creating a post
def create_new_post(*, session: Session, post: Post, author_id: int) -> Post:
    db_post = Post.model_validate(post, update={"author_id": author_id})
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# updating a post
def update_post(*, session: Session, db_post: Post, post: Post) -> Post:
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


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
