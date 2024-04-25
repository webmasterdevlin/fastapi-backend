from fastapi import APIRouter

from src.app.features.posts.models import PostsPublic


router = APIRouter()


@router.get("/", response_model=PostsPublic)
def read_posts(session= SessionDep):