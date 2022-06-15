from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from typing import Union


class PostBase(BaseModel):
    title: str
    content: Union[str, None] = None
    slug: Union[str, None] = None
    author_id: str


class PostCreate(PostBase):
    pass

class PostUnique(BaseModel):
    id: Union[str, None] = None
    slug: Union[str, None] = None

class Post(PostBase):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        orm_mode: True