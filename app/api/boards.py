from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.board import (
    BoardCreate,
    BoardResponse,
    BoardUpdate,
    BoardWithTasks
)
from app.schemas.task import TaskResponse
from app.database import (
    board_repository,
    task_repository
)
from app.database.models import User
from app.core.deps import (
    get_db,
    get_current_user,
    optional_current_user
)

router = APIRouter(prefix="/boards", tags=["boards"])


# =========================
# Get boards
# =========================

@router.get("/", response_model=List[BoardResponse])
def get_boards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách boards (projects)
    - Admin: xem tất cả
    - User: xem board của mình + public
    """
    if current_user.role == "admin":
        boards = board_repository.get_multi(db)
    else:
        boards = board_repository.get_accessible_boards(
            db,
            current_user.id
        )

    paginated = boards[skip: skip + limit]

    response: List[BoardResponse] = []

    for board in paginated:
        tasks = task_repository.get_by_board(db, board.id)

        board_resp = BoardResponse.from_orm(board)
        board_resp.tasks_count = len(tasks)

        if board.owner:
            board_resp.owner_name = (
                board.owner.full_name
                or board.owner.username
            )

        response.append(board_resp)

    return response


@router.get("/public", response_model=List[BoardResponse])
def get_public_boards(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: Optional[User] = Depends(optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Public boards (projects)
    - Không cần đăng nhập
    """
    boards = board_repository.get_public_boards(db)
    paginated = boards[skip: skip + limit]

    response: List[BoardResponse] = []

    for board in paginated:
        tasks = task_repository.get_by_board(db, board.id)

        board_resp = BoardResponse.from_orm(board)
        board_resp.tasks_count = len(tasks)

        if board.owner:
            board_resp.owner_name = (
                board.owner.full_name
                or board.owner.username
            )

        response.append(board_resp)

    return response


# =========================
# Create / Update
# =========================

@router.post(
    "/",
    response_model=BoardResponse,
    status_code=status.HTTP_201_CREATED
)
def create_board(
    board_data: BoardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Tạo board mới (Project mới để theo dõi thời gian)
    """
    board_dict = board_data.dict()
    board_dict["owner_id"] = current_user.id

    board = board_repository.create(
        db,
        obj_in=board_dict
    )

    board_resp = BoardResponse.from_orm(board)
    board_resp.tasks_count = 0
    board_resp.owner_name = (
        current_user.full_name
        or current_user.username
    )

    return board_resp


@router.get("/{board_id}", response_model=BoardWithTasks)
def get_board_detail(
    board_id: int,
    current_user: Optional[User] = Depends(optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Chi tiết board + tasks (chuẩn bị cho báo cáo theo project)
    """
    board = board_repository.get(db, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board không tồn tại"
        )

    can_access = (
        board.is_public
        or (
            current_user and (
                board.owner_id == current_user.id
                or current_user.role == "admin"
            )
        )
    )

    if not can_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền truy cập board này"
        )

    tasks = task_repository.get_by_board(db, board_id)

    board_resp = BoardWithTasks.from_orm(board)
    board_resp.tasks = [
        TaskResponse.from_orm(t)
        for t in tasks
    ]

    return board_resp


@router.put("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    board_update: BoardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cập nhật board
    """
    board = board_repository.get(db, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board không tồn tại"
        )

    if (
        board.owner_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền chỉnh sửa board này"
        )

    updated = board_repository.update(
        db,
        db_obj=board,
        obj_in=board_update
    )

    tasks = task_repository.get_by_board(db, board_id)

    board_resp = BoardResponse.from_orm(updated)
    board_resp.tasks_count = len(tasks)

    if updated.owner:
        board_resp.owner_name = (
            updated.owner.full_name
            or updated.owner.username
        )

    return board_resp


# =========================
# Delete
# =========================

@router.delete("/{board_id}")
def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Xóa board (project)
    - Không xóa time entries ở đây (sẽ xử lý bằng cascade DB)
    """
    board = board_repository.get(db, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board không tồn tại"
        )

    if (
        board.owner_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không có quyền xóa board này"
        )

    tasks = task_repository.get_by_board(db, board_id)

    board_repository.delete(db, id=board_id)

    return {
        "message": f"Đã xóa board '{board.name}'",
        "deleted_tasks_count": len(tasks)
    }