"""
CRUD операции

Содержит все операции для работы с базой данных.
"""

from .user import get_user, get_user_by_email, create_user, authenticate_user
from .post import (
    get_posts, get_post, create_post, increment_post_views,
    get_posts_by_tag, get_last_tags, book_ticket, get_user_tickets, cancel_ticket,
    get_tickets_availability, get_posts_with_availability
)
from .comment import (
    get_comments_by_post, get_comment, create_comment, update_comment, delete_comment,
    get_comments_with_users
)

__all__ = [
    "get_user", "get_user_by_email", "create_user", "authenticate_user",
    "get_posts", "get_post", "create_post", "increment_post_views",
    "get_posts_by_tag", "get_last_tags", "book_ticket", "get_user_tickets", "cancel_ticket",
    "get_tickets_availability", "get_posts_with_availability",
    "get_comments_by_post", "get_comment", "create_comment", "update_comment", "delete_comment",
    "get_comments_with_users"
]