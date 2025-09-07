from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(40), nullable=False)
    email = Column(String(40), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=True)
    avatar_url = Column(String(200), nullable=True)
    create_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to posts through association table
    posts = relationship("Post", secondary="posts_users", back_populates="users")
    
    # Relationship to comments
    comments = relationship("Comment", back_populates="user")