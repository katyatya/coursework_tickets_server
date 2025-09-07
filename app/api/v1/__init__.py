"""
API v1 роутеры

Версия 1 API endpoints для аутентификации и работы с постами.
"""

from .auth import router as auth_router
from .posts import router as posts_router
from .comments import router as comments_router

__all__ = ["auth_router", "posts_router", "comments_router"]
