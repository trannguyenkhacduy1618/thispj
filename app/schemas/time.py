# app/schemas/time.py
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

# =========================
# Time Entry
# =========================
class TimeEntryBase(BaseModel):
    task_id: int
    note: Optional[str] = None

class TimeStart(TimeEntryBase):
    pass

class TimeStop(BaseModel):
    task_id: Optional[int] = None

class TimeEntryResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    started_at: datetime
    stopped_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    note: Optional[str] = None

    class Config:
        orm_mode = True

# =========================
# Reports
# =========================
class DailyReportResponse(BaseModel):
    date: date
    total_seconds: int
    entries: List[TimeEntryResponse]

class WeeklyReportDay(BaseModel):
    date: date
    total_seconds: int

class WeeklyReportResponse(BaseModel):
    start_date: date
    end_date: date
    days: List[WeeklyReportDay]

class TaskTimeReportResponse(BaseModel):
    task_id: int
    task_title: str
    total_seconds: int

class StatisticsResponse(BaseModel):
    total_seconds: int
    task_count: int
    average_per_day: float