from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserWithToken
from app.crud.user import create_user, get_user_by_email, authenticate_user
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserWithToken)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрация пользователя"""
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    db_user = create_user(db=db, user=user)
    
    # Create access token
    access_token = create_access_token(data={"user_id": db_user.user_id})
    
    return {
        **db_user.__dict__,
        "token": access_token
    }


@router.post("/login", response_model=UserWithToken)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Вход в систему"""
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"user_id": user.user_id})
    
    return {
        **user.__dict__,
        "token": access_token
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return current_user
