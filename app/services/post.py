from copy import copy
import datetime
from typing import Union
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models import post as postModel
from app.schemas import post as postSchema


def getPost(db: Session, postUnique: postSchema.PostUnique) -> postModel.Post:
    print(postUnique)
    post = db.query(postModel.Post).filter(
        or_(
            postModel.Post.id == postUnique["id"], 
            postModel.Post.slug == postUnique["slug"]
        )
    ).first()

    return post

def getPosts(db: Session,
    skip: int=0,
    limit: int=100,
    authorId: Union[str, None] = None
) -> list[postModel.Post]:
    return db.query(postModel.Post).filter(postModel.Post.author_id == authorId).offset(skip).limit(limit).all()


def createPost(db: Session, data: postSchema.PostCreate) -> postModel.Post:
    slug = generateSlug(copy(data.title))
    print(slug)
    data.slug = copy(data.slug) if data.slug is not None else slug
    post = postModel.Post(**data.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post



def generateSlug(value) -> str:
    date = datetime.datetime.now()

    unique = date.strftime("%Y%m%d-%H%M%S")
    return unique+'-'+value.lower().replace(' ', '-')