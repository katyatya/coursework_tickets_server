from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    title = Column(String(70), nullable=False)
    tags = Column(ARRAY(String), default=[], nullable=False)
    views_count = Column(Integer, default=0)
    image_url = Column(String(300), nullable=True)
    tickets_limit = Column(Integer, default=100, nullable=False)  # Ограничение билетов
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to users through association table
    users = relationship("User", secondary="posts_users", back_populates="posts")
    
    # Relationship to comments
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


# Association table for many-to-many relationship between users and posts
posts_users = Table(
    'posts_users',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.post_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)
