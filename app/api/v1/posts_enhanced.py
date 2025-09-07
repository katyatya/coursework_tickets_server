"""
Улучшенные API endpoints с использованием Services

Это пример того, как можно использовать Services для более сложной бизнес-логики.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.post import PostResponse, TicketBooking, TicketBookingResponse
from app.api.deps import get_current_user
from app.models.user import User
from app.services import TicketService

router = APIRouter()


@router.post("/enhanced/", response_model=dict)
def book_ticket_enhanced(
    booking: TicketBooking,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Улучшенное бронирование билета с использованием Services
    
    Включает:
    - Валидацию доступности
    - Отправку уведомлений
    - Детальную обработку ошибок
    """
    ticket_service = TicketService(db)
    
    result = ticket_service.book_ticket_with_validation(
        post_id=booking.post_id,
        user_id=current_user.user_id,
        check_availability=True,
        send_notification=True
    )
    
    if not result["success"]:
        error_code = result.get("error_code", "UNKNOWN_ERROR")
        status_code = {
            "POST_NOT_FOUND": 404,
            "SOLD_OUT": 400,
            "ALREADY_BOOKED": 400
        }.get(error_code, 400)
        
        raise HTTPException(
            status_code=status_code,
            detail=result["error"]
        )
    
    return result


@router.delete("/enhanced/")
def cancel_ticket_enhanced(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Улучшенная отмена бронирования с использованием Services
    """
    ticket_service = TicketService(db)
    
    result = ticket_service.cancel_ticket_with_validation(
        post_id=post_id,
        user_id=current_user.user_id,
        check_cancellation_policy=True
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["error"]
        )
    
    return result


@router.get("/enhanced/my-tickets/", response_model=dict)
def get_my_tickets_enhanced(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение билетов пользователя с дополнительной информацией
    """
    ticket_service = TicketService(db)
    
    result = ticket_service.get_user_tickets_with_details(
        user_id=current_user.user_id,
        include_cancelled=False
    )
    
    return result


@router.get("/enhanced/tags/{tag_name}", response_model=dict)
def get_posts_by_tag_enhanced(
    tag_name: str,
    include_analytics: bool = False,
    db: Session = Depends(get_db)
):
    """
    Получение постов по тегу с аналитикой
    """
    ticket_service = TicketService(db)
    
    result = ticket_service.get_posts_by_tag_with_analytics(
        tag_name=tag_name,
        include_analytics=include_analytics
    )
    
    return result


@router.get("/enhanced/tags/", response_model=dict)
def get_popular_tags_enhanced(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Получение популярных тегов со статистикой
    """
    ticket_service = TicketService(db)
    
    result = ticket_service.get_popular_tags_with_stats(limit=limit)
    
    return result
