from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from app.models.post import Post, posts_users
from app.schemas.post import PostCreate


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    """Получение всех постов"""
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Получение поста по ID"""
    return db.query(Post).filter(Post.post_id == post_id).first()


def create_post(db: Session, post: PostCreate) -> Post:
    """Создание нового поста"""
    db_post = Post(
        title=post.title,
        text=post.text,
        tags=post.tags,
        image_url=post.image_url,
        tickets_limit=post.tickets_limit
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def increment_post_views(db: Session, post_id: int) -> Optional[Post]:
    """Увеличение счетчика просмотров"""
    post = db.query(Post).filter(Post.post_id == post_id).first()
    if post:
        post.views_count += 1
        db.commit()
        db.refresh(post)
    return post


def get_posts_by_tag(db: Session, tag: str) -> List[Post]:
    """Получение постов по тегу"""
    from sqlalchemy import func
    return db.query(Post).filter(func.array_to_string(Post.tags, ',').contains(tag)).all()


def get_last_tags(db: Session, limit: int = 20) -> List[str]:
    """Получение популярных тегов"""
    result = db.query(
        func.unnest(Post.tags).label('tag'),
        func.sum(Post.views_count).label('total_views')
    ).group_by('tag').order_by(func.sum(Post.views_count).desc()).limit(limit).all()
    
    return [row.tag for row in result if row.tag]


def book_ticket(db: Session, post_id: int, user_id: int) -> bool:
    """Бронирование билета с проверкой доступности"""
    # Check if ticket is already booked
    existing = db.query(posts_users).filter(
        and_(posts_users.c.post_id == post_id, posts_users.c.user_id == user_id)
    ).first()
    
    if existing:
        return False  # Already booked
    
    # Check if tickets are available
    post = get_post(db, post_id)
    if not post:
        return False  # Post not found
    
    # Count booked tickets
    booked_count = db.query(posts_users).filter(
        posts_users.c.post_id == post_id
    ).count()
    
    # Check if there are available tickets
    if booked_count >= post.tickets_limit:
        return False  # No tickets available
    
    # Book the ticket
    db.execute(
        posts_users.insert().values(post_id=post_id, user_id=user_id)
    )
    db.commit()
    return True


def get_user_tickets(db: Session, user_id: int) -> List[Post]:
    """Получение билетов пользователя"""
    return db.query(Post).join(posts_users).filter(
        posts_users.c.user_id == user_id
    ).all()


def cancel_ticket(db: Session, post_id: int, user_id: int) -> bool:
    """Отмена бронирования билета"""
    result = db.execute(
        posts_users.delete().where(
            and_(posts_users.c.post_id == post_id, posts_users.c.user_id == user_id)
        )
    )
    db.commit()
    return result.rowcount > 0


def get_tickets_availability(db: Session, post_id: int, user_id: int = None) -> dict:
    """Получение информации о доступности билетов"""
    post = get_post(db, post_id)
    if not post:
        return {"available": 0, "booked": 0, "limit": 0, "is_available": False, "is_booked_by_user": False}
    
    booked_count = db.query(posts_users).filter(
        posts_users.c.post_id == post_id
    ).count()
    
    available = post.tickets_limit - booked_count
    is_available = available > 0
    
    # Проверяем, забронирован ли билет конкретным пользователем
    is_booked_by_user = False
    if user_id:
        user_booking = db.query(posts_users).filter(
            and_(posts_users.c.post_id == post_id, posts_users.c.user_id == user_id)
        ).first()
        is_booked_by_user = user_booking is not None
    
    return {
        "available": available,
        "booked": booked_count,
        "limit": post.tickets_limit,
        "is_available": is_available,
        "is_booked_by_user": is_booked_by_user
    }


def get_posts_with_availability(db: Session, skip: int = 0, limit: int = 100, user_id: int = None) -> List[dict]:
    """Получение постов с информацией о доступности билетов"""
    posts = get_posts(db, skip=skip, limit=limit)
    
    posts_with_availability = []
    for post in posts:
        availability = get_tickets_availability(db, post.post_id, user_id)
        post_data = {
            "post_id": post.post_id,
            "title": post.title,
            "text": post.text,
            "tags": post.tags,
            "views_count": post.views_count,
            "image_url": post.image_url,
            "tickets_limit": post.tickets_limit,
            "created_at": post.created_at,
            "tickets_available": availability["available"],
            "tickets_booked": availability["booked"],
            "is_available": availability["is_available"],
            "is_booked_by_user": availability["is_booked_by_user"]
        }
        posts_with_availability.append(post_data)
    
    return posts_with_availability
