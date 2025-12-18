from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List

class BoardBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Tên board không được để trống')
        if len(v.strip()) > 100:
            raise ValueError('Tên board không được quá 100 ký tự')
        return v.strip()
    
    @validator('description')
    def description_validator(cls, v):
        if v is not None and v != '':
            return v.strip()
        return v


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None

    @validator('name')
    def name_validator(cls, v):
        if v is not None and (not v or len(v.strip()) == 0):
            raise ValueError('Tên board không được để trống')
        return v.strip() if v else v
    
    @validator('description')
    def description_validator(cls, v):
        if v is not None and v != '':
            return v.strip()
        return v


class BoardResponse(BoardBase):
    id: int
    owner_id: int
    owner_name: Optional[str] = None  # Owner full_name hoặc username
    created_at: datetime
    updated_at: datetime
    tasks_count: Optional[int] = 0  # Số task trong board

    class Config:
        from_attributes = True


class BoardWithTasks(BoardResponse):
    tasks: List['TaskResponse'] = []  # Forward reference

# Thử resolve forward references (TaskResponse sẽ định nghĩa trong task.py)
try:
    from app.schemas.task import TaskResponse  # noqa: F401
    BoardWithTasks.model_rebuild()
except Exception:
    pass
