from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from app.models.post import Post
from app.services import post as postService
from sqlalchemy.orm import Session
from app.database.getdb import getDb
from app.schemas import post as postSchema
from app.services import common as commonService


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post('/')
def createPost(
    data: postSchema.PostCreate,
    db: Session = Depends(getDb)
) -> Post:
    postUnique = {
        "id": None,
        "slug": data.slug
    }
    post = postService.getPost(db, postUnique)
    if post:
        raise HTTPException(status_code=400, detail="Post already registered")
    return postService.createPost(db, data)


@router.get("/")
def listPosts(
    *,
    skip: Union[int, None] = Query(0),
    limit: Union[int, None] = Query(100),
    authorId: Union[str, None] = None,
    db: Session = Depends(getDb)
) -> list[Post]:
    return postService.getPosts(db, skip, limit, authorId)


@router.get("/{postId}")
def getPost(
    postId: str = Path(...),
    db: Session = Depends(getDb)
) -> Post:
    postUnique = {
        'id': postId if commonService.isValidUUID(postId) else None,
        'slug': postId
    }
    return postService.getPost(db, postUnique)