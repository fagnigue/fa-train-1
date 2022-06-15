from datetime import datetime
from typing import Union
from uuid import UUID
from pydantic import BaseModel

from app.models.post import Post

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    nickname: str

class UserUnique(BaseModel):
    id: Union[str, None]
    email: Union[str, None]

class User(UserBase):
    nickname: str
    is_verified: bool
    created_at: datetime
    posts = list[Post]

    class Config:
        orm_mode = True
