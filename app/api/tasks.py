from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskMove,
    TaskAssign
)
from app.database import (
    task_repository,
    board_repository,
    user_repository
)
from app.database.models import User, StatusEnum
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


# =========================
# Helper: board permission
# =========================

def check_board_access(
    db: Session,
    board_id: int,
    user: User,
    action: str = "read"
) -> bool:
    board = board_repository.get(db, board_id)
    if not board:
        return False

    if user.role == "admin":
        return True

    if board.owner_id == user.id:
        return True

    if board.is_public and action == "read":
        return True

    return False


# =========================
# Get tasks
# =========================

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    board_id: int = Query(..., description="Board (Project) ID"),
    status: Optional[str] = Query(None),
    assigned_to: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách tasks trong board
    (sử dụng cho task list + time tracking)
    """
    board = board_repository.get(db, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board không tồn tại"
        )

    if not check_board_access(db, board_id, current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập board này"
        )

    if status:
        try:
            status_enum = StatusEnum(status)
            tasks = task_repository.get_by_status(
                db,
                board_id,
                status_enum
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Status không hợp lệ"
            )
    else:
        tasks = task_repository.get_by_board(db, board_id)

    if assigned_to is not None:
        tasks = [
            t for t in tasks
            if t.assigned_to == assigned_to
        ]

    return [TaskResponse.from_orm(t) for t in tasks]


# =========================
# Create task
# =========================

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Tạo task mới (task sẽ là đơn vị theo dõi thời gian)
    """
    if not check_board_access(
        db,
        task_data.board_id,
        current_user,
        "write"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền tạo task"
        )

    existing = task_repository.get_by_status(
        db,
        task_data.board_id,
        task_data.status
    )

    task_dict = task_data.dict()
    task_dict["position"] = len(existing)

    task = task_repository.create(
        db,
        obj_in=task_dict
    )

    return TaskResponse.from_orm(task)


# =========================
# Task detail
# =========================

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy chi tiết task (frontend sẽ dùng để hiển thị stopwatch)
    """
    task = task_repository.get(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    if not check_board_access(
        db,
        task.board_id,
        current_user,
        "read"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập task"
        )

    return TaskResponse.from_orm(task)


# =========================
# Update task
# =========================

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cập nhật task
    """
    task = task_repository.get(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    if not check_board_access(
        db,
        task.board_id,
        current_user,
        "write"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền chỉnh sửa task"
        )

    updated = task_repository.update(
        db,
        db_obj=task,
        obj_in=task_update
    )

    return TaskResponse.from_orm(updated)


# =========================
# Move task (kanban logic)
# =========================

@router.patch("/{task_id}/move", response_model=TaskResponse)
def move_task(
    task_id: int,
    task_move: TaskMove,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Di chuyển task (giữ lại để không phá UI cũ)
    """
    task = task_repository.get(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    if not check_board_access(
        db,
        task.board_id,
        current_user,
        "write"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền di chuyển task"
        )

    moved = task_repository.move_task(
        db,
        task_id,
        task_move.status,
        task_move.position
    )

    return TaskResponse.from_orm(moved)


# =========================
# Assign task
# =========================

@router.patch("/{task_id}/assign", response_model=TaskResponse)
def assign_task(
    task_id: int,
    task_assign: TaskAssign,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Gán task cho user (ai được assign sẽ là người bấm giờ)
    """
    task = task_repository.get(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    if not check_board_access(
        db,
        task.board_id,
        current_user,
        "write"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền assign task"
        )

    if task_assign.assigned_to:
        user = user_repository.get(
            db,
            task_assign.assigned_to
        )
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User được assign không hợp lệ"
            )

    updated = task_repository.update(
        db,
        db_obj=task,
        obj_in={"assigned_to": task_assign.assigned_to}
    )

    return TaskResponse.from_orm(updated)


# =========================
# Delete task
# =========================

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Xóa task (time entries sẽ bị xóa bằng cascade)
    """
    task = task_repository.get(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    if not check_board_access(
        db,
        task.board_id,
        current_user,
        "write"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xóa task"
        )

    task_repository.delete(db, id=task_id)

    return {
        "message": f"Đã xóa task '{task.title}'",
        "task_id": task_id
    }


# =========================
# My assigned tasks
# =========================

@router.get("/my/assigned", response_model=List[TaskResponse])
def get_my_assigned_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Tasks được assign cho user hiện tại (dashboard + thống kê thời gian)
    """
    if current_user.role == "admin":
        tasks = task_repository.get_multi(db)
    else:
        tasks = task_repository.get_by_assigned_user(
            db,
            current_user.id
        )

    return [TaskResponse.from_orm(t) for t in tasks]