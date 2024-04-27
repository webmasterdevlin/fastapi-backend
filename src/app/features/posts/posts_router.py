from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select, func

from .services import create_new_post
from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostCreate, PostsPublic

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


# 404 or 200 response
@router.get("/posts/{post_id}", response_model=Post, tags=["posts"])
def read_post_by_id(session: SessionDep, post_id: int) -> Any:
    """
    Retrieve a post by id using a url parameter post_id.
    """
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post not found"})
    return post


@router.post("/posts", response_model=Post, tags=["posts"])
def create_post(session: SessionDep, post: PostCreate, author_id: int) -> Any:
    """
    Create a post using a request body post and a query parameter author_id.
    """
    return create_new_post(
        session=session,
        post=post,
        author_id=author_id,  # type: ignore
    )


# 4. Add a route to update a post
@router.put("/posts/{post_id}", response_model=Post)
def update_post(session: SessionDep, post_id: int, updated_post: Post) -> Any:
    """
    Update a post using a url parameter post_id and a request body updated_post.
    """
    updated_post = session.get(Post, post_id)  # type: ignore
    if not updated_post:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = updated_post.model_dump(exclude_unset=True)
    updated_post.sqlmodel_update(update_dict)
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    return updated_post


# 5. Add a route to delete a post
@router.delete("/posts/{post_id}", response_model=None)
def delete_post(session: SessionDep, post_id: int) -> Any:
    """
    Delete a post using a url parameter post_id.
    """
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post not found"})
    else:
        session.delete(post)
        session.commit()
        return None
