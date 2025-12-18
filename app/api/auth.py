from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.core.config import settings
from app.core.deps import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.database import user_repository

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=dict)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Login bằng OAuth2 form (username & password)
    Trả về JWT access token
    """
    user = user_repository.get_by_username(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị khóa",
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user),
    }


@router.post("/login-json", response_model=dict)
def login_json(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login bằng JSON payload
    Dùng cho frontend SPA / mobile app
    """
    user = user_repository.get_by_username(db, user_data.username)

    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đã bị khóa",
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        subject=user.id,
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user),
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Đăng ký user mới
    """
    # Check username
    if user_repository.get_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username đã tồn tại",
        )

    # Check email
    if user_data.email:
        if user_repository.get_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email đã tồn tại",
            )

    user_dict = user_data.dict()
    user_dict["password_hash"] = get_password_hash(user_data.password)
    user_dict.pop("password", None)

    user = user_repository.create_user(db, user_dict)

    return UserResponse.from_orm(user)
