from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    user_id: int
    create_timestamp: datetime
    
    class Config:
        from_attributes = True


class UserResponse(User):
    pass


class UserWithToken(User):
    token: str
