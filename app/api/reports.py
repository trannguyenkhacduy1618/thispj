from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, time_entry_repository, task_repository
from app.database.models import User
from app.schemas.time import (
    DailyReportResponse,
    WeeklyReportResponse,
    TaskTimeReportResponse,
    StatisticsResponse,
)
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

# =========================
# Daily report
# =========================

@router.get("/daily", response_model=DailyReportResponse)
def daily_report(
    report_date: date = Query(default=date.today()),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Báo cáo thời gian làm việc theo ngày
    """

    entries = time_entry_repository.get_by_user_and_date(
        db,
        user_id=current_user.id,
        report_date=report_date
    )

    total_seconds = sum(e.duration_seconds for e in entries)

    return DailyReportResponse(
        date=report_date,
        total_seconds=total_seconds,
        entries=entries
    )


# =========================
# Weekly report
# =========================

@router.get("/weekly", response_model=WeeklyReportResponse)
def weekly_report(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Báo cáo thời gian làm việc theo tuần / khoảng ngày
    """

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date phải nhỏ hơn end_date"
        )

    data = time_entry_repository.get_group_by_date(
        db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return WeeklyReportResponse(
        start_date=start_date,
        end_date=end_date,
        days=data
    )


# =========================
# Report by task
# =========================

@router.get("/by-task", response_model=List[TaskTimeReportResponse])
def report_by_task(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Báo cáo tổng thời gian theo từng task
    """

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date phải nhỏ hơn end_date"
        )

    stats = time_entry_repository.get_group_by_task(
        db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return stats


# =========================
# Summary statistics
# =========================

@router.get("/summary", response_model=StatisticsResponse)
def summary_statistics(
    start_date: date = Query(...),
    end_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Thống kê tổng hợp:
    - Tổng thời gian
    - Số task
    - Trung bình / ngày
    """

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date phải nhỏ hơn end_date"
        )

    stats = time_entry_repository.statistics(
        db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )

    return stats
