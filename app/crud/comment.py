from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
    """Получение комментариев к посту"""
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    """Получение комментария по ID"""
    return db.query(Comment).filter(Comment.comment_id == comment_id).first()


def create_comment(db: Session, comment: CommentCreate, user_id: int) -> Comment:
    """Создание нового комментария"""
    db_comment = Comment(
        text=comment.text,
        post_id=comment.post_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate, user_id: int) -> Optional[Comment]:
    """Обновление комментария (только автором)"""
    comment = db.query(Comment).filter(
        and_(Comment.comment_id == comment_id, Comment.user_id == user_id)
    ).first()
    
    if not comment:
        return None
    
    if comment_update.text is not None:
        comment.text = comment_update.text
    
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int, user_id: int) -> bool:
    """Удаление комментария (только автором)"""
    comment = db.query(Comment).filter(
        and_(Comment.comment_id == comment_id, Comment.user_id == user_id)
    ).first()
    
    if not comment:
        return False
    
    db.delete(comment)
    db.commit()
    return True


def get_comments_with_users(db: Session, post_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """Получение комментариев с информацией о пользователях"""
    comments = db.query(Comment).options(joinedload(Comment.user)).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
    
    comments_with_users = []
    for comment in comments:
        comment_data = {
            "comment_id": comment.comment_id,
            "text": comment.text,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "created_at": comment.created_at,
            "user": {
                "user_id": comment.user.user_id,
                "full_name": comment.user.full_name,
                "avatar_url": comment.user.avatar_url
            }
        }
        comments_with_users.append(comment_data)
    
    return comments_with_users
