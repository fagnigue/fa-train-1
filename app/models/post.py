from enum import unique
from operator import index
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base



class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    slug = Column(String, unique=True, index=True)
    title = Column(String)
    content = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, default=func.now())
    author_id = Column(UUID, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")

