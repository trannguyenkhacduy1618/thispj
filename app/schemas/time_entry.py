from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class TimeEntryBase(BaseModel):
    task_id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    notes: Optional[str] = None

    @validator("end_time")
    def validate_end_time(cls, v, values):
        if v and "start_time" in values and v < values["start_time"]:
            raise ValueError("end_time không thể trước start_time")
        return v


class TimeEntryCreate(TimeEntryBase):
    pass


class TimeEntryUpdate(BaseModel):
    end_time: Optional[datetime] = None
    notes: Optional[str] = None


class TimeEntryResponse(TimeEntryBase):
    id: int
    duration_seconds: Optional[int] = None  # Có thể tính từ end_time - start_time
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
