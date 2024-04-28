from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from .services import create_new_post, get_all_posts, get_post_by_id, update_post
from src.app.helpers.dependencies import SessionDep
from src.app.schemas.models import Post, PostCreate, PostsPublic

router = APIRouter()


@router.get("/posts", response_model=PostsPublic, tags=["posts"])
def read_posts(
    session: SessionDep, author_id: int, skip: int = 0, limit: int = 10
) -> Any:
    """
    Retrieve posts by author ID.

    Args:
        session (SessionDep): The database session dependency.
        author_id (int): The ID of the author.
        skip (int, optional): Number of posts to skip. Defaults to 0.
        limit (int, optional): Maximum number of posts to retrieve. Defaults to 10.

    Returns:
        Any: The retrieved posts or a JSON response with an error message if the author does not exist.
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
    Retrieve a post by its ID.

    Args:
        session (SessionDep): The database session dependency.
        post_id (int): The ID of the post to retrieve.

    Returns:
        Any: The retrieved post.

    Raises:
        JSONResponse: If the post is not found.
    """
    post = get_post_by_id(
        session=session, post_id=post_id
    )  # session.get(Post, post_id) is the same as get_post_by_id but with less error handling
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post not found"})
    return post


@router.post("/posts", response_model=Post, tags=["posts"])
def create_post(session: SessionDep, post: PostCreate, author_id: int) -> Any:
    """
    Create a new post.

    Args:
        session (SessionDep): The database session.
        post (PostCreate): The data for the new post.
        author_id (int): The ID of the post's author.

    Returns:
        Any: The created post.
    """
    return create_new_post(
        session=session,
        post=post,
        author_id=author_id,  # type: ignore
    )


@router.put("/posts/{post_id}", response_model=Post, tags=["posts"])
def update_post_by_id(session: SessionDep, post_id: int, updated_post: Post) -> Any:
    """
    Update a post by its ID.

    Args:
        session (SessionDep): The database session dependency.
        post_id (int): The ID of the post to be updated.
        updated_post (Post): The updated post data.

    Returns:
        Any: The updated post.

    Raises:
        HTTPException: If the post with the given ID is not found.
    """
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Item not found")

    return update_post(session=session, post=post, updated_post=updated_post)


@router.delete("/posts/{post_id}", tags=["posts"])
def delete_post(session: SessionDep, post_id: int) -> JSONResponse:
    """
    Delete a post with the given post_id.

    Args:
        session (SessionDep): The database session dependency.
        post_id (int): The ID of the post to be deleted.

    Returns:
        JSONResponse: A JSON response indicating the status of the deletion.
            If the post is found and successfully deleted, returns a 204 status code
            with a message indicating the deletion. If the post is not found,
            returns a 404 status code with a message indicating that the post was not found.
    """
    post = session.get(Post, post_id)
    if post is None:
        return JSONResponse(status_code=404, content={"message": "Post not found"})
    else:
        session.delete(post)
        session.commit()
        return JSONResponse(status_code=204, content={"message": "Post deleted"})
