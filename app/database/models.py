from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# ====================
# ENUMS
# ====================
class StatusEnum(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

# ====================
# USER
# ====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(10), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    boards = relationship("Board", back_populates="owner")
    tasks = relationship("Task", back_populates="assigned_user")
    time_entries = relationship("TimeTracking", back_populates="user")

# ====================
# BOARD
# ====================
class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="boards")
    tasks = relationship("Task", back_populates="board")

# ====================
# TASK
# ====================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.todo)
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.medium)
    position = Column(Integer, default=0)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    board = relationship("Board", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
    time_entries = relationship("TimeTracking", back_populates="task")

# ====================
# TIME TRACKING
# ====================
class TimeTracking(Base):
    __tablename__ = "time_tracking"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)  # None nếu đang chạy
    duration_seconds = Column(Integer, nullable=True)  # total seconds

    task = relationship("Task", back_populates="time_entries")
    user = relationship("User", back_populates="time_entries")

# ====================
# REPORT
# ====================
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    report_date = Column(DateTime, nullable=False)
    total_seconds = Column(Integer, default=0)
    task_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
