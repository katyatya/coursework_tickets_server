from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    text: str
    tags: List[str] = []
    image_url: Optional[str] = None
    tickets_limit: int = 100


class PostCreate(PostBase):
    pass


class Post(PostBase):
    post_id: int
    views_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostResponse(Post):
    tickets_available: int = 0
    tickets_booked: int = 0
    is_available: bool = True
    is_booked_by_user: bool = False


class TicketBooking(BaseModel):
    post_id: int


class TicketBookingResponse(BaseModel):
    post_id: int
    user_id: int
    
    class Config:
        from_attributes = True


class PostWithAvailability(Post):
    """Пост с информацией о доступности билетов"""
    tickets_available: int
    tickets_booked: int
    is_available: bool
