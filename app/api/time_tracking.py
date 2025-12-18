from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import (
    task_repository,
    user_repository,
    time_entry_repository,
)
from app.database.models import User
from app.schemas.time import (
    TimeEntryResponse,
    TimeStart,
    TimeStop,
    DailyReportResponse,
    StatisticsResponse,
)
from app.core.deps import get_db, get_current_user

router = APIRouter(
    prefix="/time",
    tags=["time-tracking"]
)

# =========================
# START stopwatch
# =========================

@router.post("/start", response_model=TimeEntryResponse)
def start_timer(
    payload: TimeStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Bắt đầu bấm giờ cho 1 task
    - 1 user chỉ được chạy 1 timer tại 1 thời điểm
    """
    task = task_repository.get(db, payload.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )

    # Kiểm tra task có được assign cho user không
    if task.assigned_to and task.assigned_to != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không được assign task này"
        )

    # Kiểm tra timer đang chạy
    running = time_entry_repository.get_running_by_user(
        db,
        current_user.id
    )
    if running:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bạn đang bấm giờ cho task khác"
        )

    entry = time_entry_repository.start(
        db=db,
        user_id=current_user.id,
        task_id=payload.task_id,
        started_at=datetime.utcnow(),
        note=payload.note
    )

    return TimeEntryResponse.from_orm(entry)


# =========================
# STOP stopwatch
# =========================

@router.post("/stop", response_model=TimeEntryResponse)
def stop_timer(
    payload: TimeStop,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dừng stopwatch"""
    entry = time_entry_repository.get_running_by_user(
        db,
        current_user.id
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có timer đang chạy"
        )

    if payload.task_id and entry.task_id != payload.task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task không khớp với timer đang chạy"
        )

    stopped = time_entry_repository.stop(
        db=db,
        entry=entry,
        stopped_at=datetime.utcnow()
    )

    return TimeEntryResponse.from_orm(stopped)


# =========================
# My running timer
# =========================

@router.get("/running", response_model=Optional[TimeEntryResponse])
def get_running_timer(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lấy timer đang chạy (frontend polling)"""
    entry = time_entry_repository.get_running_by_user(
        db,
        current_user.id
    )

    if not entry:
        return None

    return TimeEntryResponse.from_orm(entry)


# =========================
# Daily report
# =========================

@router.get("/daily-report", response_model=DailyReportResponse)
def daily_report(
    report_date: date = Query(default=date.today()),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Báo cáo thời gian làm việc theo ngày"""
    entries = time_entry_repository.get_by_user_and_date(
        db,
        user_id=current_user.id,
        report_date=report_date
    )

    total_seconds = sum(e.duration_seconds for e in entries)

    return DailyReportResponse(
        date=report_date,
        total_seconds=total_seconds,
        entries=[TimeEntryResponse.from_orm(e) for e in entries]
    )


# =========================
# Statistics
# =========================

@router.get("/statistics", response_model=StatisticsResponse)
def statistics(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Thống kê thời gian làm việc
    - Theo task
    - Theo ngày
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ngày bắt đầu phải nhỏ hơn ngày kết thúc"
        )

    stats = time_entry_repository.statistics(
        db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return stats