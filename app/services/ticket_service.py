"""
Сервис для работы с билетами

Содержит бизнес-логику для бронирования, отмены и управления билетами.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.post import (
    get_post, book_ticket, cancel_ticket, get_user_tickets,
    get_posts_by_tag, get_last_tags
)
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostResponse, TicketBookingResponse


class TicketService:
    """Сервис для работы с билетами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def book_ticket_with_validation(
        self, 
        post_id: int, 
        user_id: int,
        check_availability: bool = True,
        send_notification: bool = False
    ) -> Dict[str, Any]:
        """
        Бронирование билета с дополнительной валидацией
        
        Args:
            post_id: ID поста/события
            user_id: ID пользователя
            check_availability: Проверять ли доступность
            send_notification: Отправлять ли уведомление
            
        Returns:
            Результат бронирования
        """
        # 1. Проверяем существование поста
        post = get_post(self.db, post_id)
        if not post:
            return {
                "success": False,
                "error": "Post not found",
                "error_code": "POST_NOT_FOUND"
            }
        
        # 2. Проверяем доступность (если требуется)
        if check_availability:
            # Здесь можно добавить логику проверки лимитов, дат и т.д.
            if post.views_count > 1000:  # Пример: лимит просмотров
                return {
                    "success": False,
                    "error": "Event is sold out",
                    "error_code": "SOLD_OUT"
                }
        
        # 3. Пытаемся забронировать
        success = book_ticket(self.db, post_id, user_id)
        if not success:
            return {
                "success": False,
                "error": "Ticket already booked",
                "error_code": "ALREADY_BOOKED"
            }
        
        # 4. Отправляем уведомление (если требуется)
        if send_notification:
            self._send_booking_notification(user_id, post)
        
        # 5. Возвращаем успешный результат
        return {
            "success": True,
            "data": TicketBookingResponse(post_id=post_id, user_id=user_id),
            "message": "Ticket booked successfully"
        }
    
    def cancel_ticket_with_validation(
        self, 
        post_id: int, 
        user_id: int,
        check_cancellation_policy: bool = True
    ) -> Dict[str, Any]:
        """
        Отмена бронирования с проверкой политики отмены
        """
        # 1. Проверяем политику отмены
        if check_cancellation_policy:
            post = get_post(self.db, post_id)
            if post:
                # Пример: нельзя отменить за 24 часа до события
                # Здесь можно добавить проверку даты события
                pass
        
        # 2. Отменяем бронирование
        success = cancel_ticket(self.db, post_id, user_id)
        if not success:
            return {
                "success": False,
                "error": "Ticket not found or already cancelled",
                "error_code": "TICKET_NOT_FOUND"
            }
        
        return {
            "success": True,
            "message": "Ticket cancelled successfully"
        }
    
    def get_user_tickets_with_details(
        self, 
        user_id: int,
        include_cancelled: bool = False
    ) -> Dict[str, Any]:
        """
        Получение билетов пользователя с дополнительной информацией
        """
        tickets = get_user_tickets(self.db, user_id)
        
        # Добавляем дополнительную информацию
        ticket_details = []
        for ticket in tickets:
            ticket_info = {
                "post_id": ticket.post_id,
                "title": ticket.title,
                "created_at": ticket.created_at,
                "views_count": ticket.views_count,
                "tags": ticket.tags,
                "image_url": ticket.image_url,
                # Можно добавить статус, дату события и т.д.
                "status": "active"  # Пример
            }
            ticket_details.append(ticket_info)
        
        return {
            "success": True,
            "data": ticket_details,
            "count": len(ticket_details)
        }
    
    def get_posts_by_tag_with_analytics(
        self, 
        tag_name: str,
        include_analytics: bool = False
    ) -> Dict[str, Any]:
        """
        Получение постов по тегу с аналитикой
        """
        posts = get_posts_by_tag(self.db, tag_name)
        
        result = {
            "success": True,
            "data": posts,
            "count": len(posts)
        }
        
        if include_analytics:
            # Добавляем аналитику
            total_views = sum(post.views_count for post in posts)
            result["analytics"] = {
                "total_views": total_views,
                "average_views": total_views / len(posts) if posts else 0,
                "most_popular": max(posts, key=lambda p: p.views_count).title if posts else None
            }
        
        return result
    
    def _send_booking_notification(self, user_id: int, post: Post) -> None:
        """
        Отправка уведомления о бронировании (заглушка)
        """
        # Здесь можно добавить логику отправки email, push-уведомлений и т.д.
        print(f"Notification sent to user {user_id} about booking {post.title}")
    
    def get_popular_tags_with_stats(self, limit: int = 10) -> Dict[str, Any]:
        """
        Получение популярных тегов со статистикой
        """
        tags = get_last_tags(self.db, limit)
        
        # Добавляем статистику для каждого тега
        tag_stats = []
        for tag in tags:
            posts_count = len(get_posts_by_tag(self.db, tag))
            tag_stats.append({
                "name": tag,
                "posts_count": posts_count
            })
        
        return {
            "success": True,
            "data": tag_stats,
            "total_tags": len(tag_stats)
        }
