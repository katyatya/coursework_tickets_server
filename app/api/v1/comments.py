from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.comment import Comment, CommentCreate, CommentUpdate, CommentWithUser
from app.crud.comment import (
    get_comments_by_post, get_comment, create_comment, update_comment, delete_comment,
    get_comments_with_users
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/post/{post_id}", response_model=List[CommentWithUser])
def get_post_comments(
    post_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Получение комментариев к посту"""
    comments = get_comments_with_users(db, post_id, skip=skip, limit=limit)
    return comments


@router.post("/", response_model=CommentWithUser)
def create_new_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создание нового комментария (требует авторизации)"""
    # Проверяем, что пост существует
    from app.crud.post import get_post
    post = get_post(db, comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Создаем комментарий
    db_comment = create_comment(db, comment, current_user.user_id)
    
    # Возвращаем комментарий с информацией о пользователе
    comment_with_user = {
        "comment_id": db_comment.comment_id,
        "text": db_comment.text,
        "post_id": db_comment.post_id,
        "user_id": db_comment.user_id,
        "created_at": db_comment.created_at,
        "user": {
            "user_id": current_user.user_id,
            "full_name": current_user.full_name,
            "avatar_url": current_user.avatar_url
        }
    }
    return comment_with_user


@router.get("/{comment_id}", response_model=Comment)
def get_comment_by_id(comment_id: int, db: Session = Depends(get_db)):
    """Получение комментария по ID"""
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentWithUser)
def update_comment_by_id(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Обновление комментария (только автором)"""
    updated_comment = update_comment(db, comment_id, comment_update, current_user.user_id)
    if not updated_comment:
        raise HTTPException(
            status_code=404, 
            detail="Comment not found or you don't have permission to edit it"
        )
    
    # Возвращаем комментарий с информацией о пользователе
    comment_with_user = {
        "comment_id": updated_comment.comment_id,
        "text": updated_comment.text,
        "post_id": updated_comment.post_id,
        "user_id": updated_comment.user_id,
        "created_at": updated_comment.created_at,
        "user": {
            "user_id": current_user.user_id,
            "full_name": current_user.full_name,
            "avatar_url": current_user.avatar_url
        }
    }
    return comment_with_user


@router.delete("/{comment_id}")
def delete_comment_by_id(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Удаление комментария (только автором)"""
    success = delete_comment(db, comment_id, current_user.user_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Comment not found or you don't have permission to delete it"
        )
    return {"message": "Comment deleted successfully"}
