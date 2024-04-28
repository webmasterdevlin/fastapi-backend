from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select, func

from .services import create_new_post, get_all_posts, get_post_by_id
from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostCreate, PostsPublic

router = APIRouter()


@router.get("/posts", response_model=PostsPublic, tags=["posts"])
def read_posts(
    session: SessionDep, author_id: int, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve posts with query parameters author_id, skip, and limit.
    """
    posts = get_all_posts(session=session, author_id=author_id, skip=skip, limit=limit)
    if posts is None:
        return JSONResponse(
            status_code=404, content={"message": "Author does not exist"}
        )
    return posts


@router.get("/posts/{post_id}", response_model=Post, tags=["posts"])
def read_post_by_id(session: SessionDep, post_id: int) -> Any:
    """
    Retrieve a post by id using a url parameter post_id.
    """
    post = get_post_by_id(session=session, post_id=post_id)
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


# TODO FIX THIS
@router.put("/posts/{post_id}", response_model=Post)
def update_post(session: SessionDep, post_id: int, updated_post: Post) -> Any:
    """
    Update a post using a url parameter post_id and a request body updated_post.
    """
    post = get_post_by_id(session=session, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Item not found")

    update_dict = updated_post.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_dict)
    session.commit()
    session.refresh(post)
    return post


@router.delete("/posts/{post_id}")
def delete_post(session: SessionDep, post_id: int) -> JSONResponse:
    """
    Delete a post using a url parameter post_id.
    """
    post = get_post_by_id(session=session, post_id=post_id)
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post not found"})
    else:
        session.delete(post)
        session.commit()
        return JSONResponse(status_code=204, content={"message": "Post deleted"})
