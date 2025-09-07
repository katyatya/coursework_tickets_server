from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class CommentInDBBase(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Comment(CommentInDBBase):
    pass


class CommentWithUser(CommentInDBBase):
    user: dict  # Будет содержать информацию о пользователе
