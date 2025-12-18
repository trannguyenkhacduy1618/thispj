from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import (
    UserResponse,
    UserUpdate,
    PasswordChange
)
from app.database import get_db, user_repository
from app.database.models import User
from app.core.deps import (
    get_current_user,
    get_current_admin_user
)
from app.core.security import verify_password

router = APIRouter(prefix="/users", tags=["users"])


# =========================
# Current user
# =========================

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Lấy thông tin user hiện tại
    """
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cập nhật thông tin cá nhân
    - Không cho user thường đổi role
    """
    update_data = user_update.dict(exclude_unset=True)

    if "role" in update_data and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền thay đổi role"
        )

    # Email conflict
    if user_update.email and user_update.email != current_user.email:
        existing = user_repository.get_by_email(db, user_update.email)
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email đã được sử dụng"
            )

    updated_user = user_repository.update(
        db,
        db_obj=current_user,
        obj_in=update_data
    )

    return UserResponse.from_orm(updated_user)


@router.patch("/me/password")
def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Đổi mật khẩu user hiện tại
    """
    if not verify_password(
        password_change.current_password,
        current_user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mật khẩu hiện tại không đúng"
        )

    user_repository.update_password(
        db,
        current_user,
        password_change.new_password
    )

    return {"message": "Đổi mật khẩu thành công"}


# =========================
# User list (for assign & report)
# =========================

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách users
    - Dùng cho assign task
    - Dùng cho thống kê time tracking
    """
    users = user_repository.get_multi(
        db,
        skip=skip,
        limit=limit
    )
    return [UserResponse.from_orm(u) for u in users]


# =========================
# Admin only
# =========================

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin lấy thông tin user bất kỳ
    """
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại"
        )

    return UserResponse.from_orm(user)


@router.put("/{user_id}", response_model=UserResponse)
def admin_update_user(
    user_id: int,
    user_update: UserUpdate,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin cập nhật user:
    - role
    - is_active
    - email
    """
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại"
        )

    update_data = user_update.dict(exclude_unset=True)

    # Email conflict
    if user_update.email and user_update.email != user.email:
        existing = user_repository.get_by_email(db, user_update.email)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email đã được sử dụng"
            )

    updated_user = user_repository.update(
        db,
        db_obj=user,
        obj_in=update_data
    )

    return UserResponse.from_orm(updated_user)


@router.delete("/{user_id}")
def admin_delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin xóa user
    """
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User không tồn tại"
        )

    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể xóa chính mình"
        )

    user_repository.delete(db, id=user_id)

    return {
        "message": f"Đã xóa user {user.username}",
        "deleted_user_id": user_id
    }
