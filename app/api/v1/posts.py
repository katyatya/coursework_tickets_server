from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from app.database import get_db
from app.schemas.post import PostResponse, TicketBooking, TicketBookingResponse
from app.crud.post import (
    get_posts, get_post, increment_post_views, get_posts_by_tag, 
    get_last_tags, book_ticket, get_user_tickets, cancel_ticket,
    get_tickets_availability, get_posts_with_availability
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[PostResponse])
def get_all_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение всех постов с информацией о доступности билетов"""
    posts = get_posts_with_availability(db, skip=skip, limit=limit)
    return posts


@router.get("/with-availability/")
def get_posts_with_availability_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение всех постов с информацией о доступности билетов"""
    posts = get_posts_with_availability(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
def get_one_post(post_id: int, db: Session = Depends(get_db)):
    """Получение конкретного поста с информацией о доступности билетов"""
    post = increment_post_views(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Получаем информацию о доступности билетов
    availability = get_tickets_availability(db, post_id)
    
    # Создаем объект с полной информацией
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
        "is_available": availability["is_available"]
    }
    
    return post_data


@router.get("/{post_id}/availability/")
def get_post_availability(post_id: int, db: Session = Depends(get_db)):
    """Получение информации о доступности билетов для конкретного поста"""
    availability = get_tickets_availability(db, post_id)
    if availability["limit"] == 0:
        raise HTTPException(status_code=404, detail="Post not found")
    return availability


@router.get("/tags/{tag_name}", response_model=List[PostResponse])
def get_posts_by_tag_name(tag_name: str, db: Session = Depends(get_db)):
    """Получение постов по тегу с информацией о доступности билетов"""
    try:
        # Декодируем URL-encoded символы
        import urllib.parse
        decoded_tag = urllib.parse.unquote(tag_name)
        posts = get_posts_by_tag(db, decoded_tag)
        
        # Добавляем информацию о доступности для каждого поста
        posts_with_availability = []
        for post in posts:
            availability = get_tickets_availability(db, post.post_id)
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
                "is_available": availability["is_available"]
            }
            posts_with_availability.append(post_data)
        
        return posts_with_availability
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing tag: {str(e)}")


@router.post("/", response_model=TicketBookingResponse)
def book_ticket_endpoint(
    booking: TicketBooking,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Бронирование билета с проверкой доступности"""
    # Verify post exists
    post = get_post(db, booking.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check availability first
    availability = get_tickets_availability(db, booking.post_id)
    if not availability["is_available"]:
        raise HTTPException(
            status_code=400, 
            detail=f"No tickets available. {availability['booked']}/{availability['limit']} tickets booked"
        )
    
    # Book the ticket
    success = book_ticket(db, booking.post_id, current_user.user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Ticket already booked by this user")
    
    return TicketBookingResponse(post_id=booking.post_id, user_id=current_user.user_id)


@router.delete("/")
def cancel_ticket_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Отмена бронирования билета"""
    success = cancel_ticket(db, post_id, current_user.user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return {"message": "success"}


@router.get("/my-tickets/", response_model=List[PostResponse])
def get_my_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получение билетов текущего пользователя с информацией о доступности"""
    tickets = get_user_tickets(db, current_user.user_id)
    
    # Добавляем информацию о доступности для каждого билета
    tickets_with_availability = []
    for ticket in tickets:
        availability = get_tickets_availability(db, ticket.post_id)
        ticket_data = {
            "post_id": ticket.post_id,
            "title": ticket.title,
            "text": ticket.text,
            "tags": ticket.tags,
            "views_count": ticket.views_count,
            "image_url": ticket.image_url,
            "tickets_limit": ticket.tickets_limit,
            "created_at": ticket.created_at,
            "tickets_available": availability["available"],
            "tickets_booked": availability["booked"],
            "is_available": availability["is_available"]
        }
        tickets_with_availability.append(ticket_data)
    
    return tickets_with_availability


@router.get("/tags/", response_model=List[str])
def get_tags(db: Session = Depends(get_db)):
    """Получение популярных тегов"""
    tags = get_last_tags(db)
    return tags


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """Загрузка файла"""
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"url": f"/uploads/{file.filename}"}
