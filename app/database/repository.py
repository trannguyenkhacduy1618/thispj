from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.database.models import User, Board, Task, TimeTracking, Report, StatusEnum, PriorityEnum

# ====================
# USER REPOSITORY
# ====================
class UserRepository:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user_dict: dict) -> User:
        user = User(**user_dict)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, obj_in: dict) -> User:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_password(self, db: Session, user: User, new_password_hash: str):
        user.password_hash = new_password_hash
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, id: int):
        db.query(User).filter(User.id == id).delete()
        db.commit()


user_repository = UserRepository()


# ====================
# BOARD REPOSITORY
# ====================
class BoardRepository:
    def get(self, db: Session, board_id: int) -> Optional[Board]:
        return db.query(Board).filter(Board.id == board_id).first()

    def get_multi(self, db: Session) -> List[Board]:
        return db.query(Board).all()

    def get_public_boards(self, db: Session) -> List[Board]:
        return db.query(Board).filter(Board.is_public == True).all()

    def get_accessible_boards(self, db: Session, user_id: int) -> List[Board]:
        return db.query(Board).filter(
            (Board.owner_id == user_id) | (Board.is_public == True)
        ).all()

    def create(self, db: Session, obj_in: dict) -> Board:
        board = Board(**obj_in)
        db.add(board)
        db.commit()
        db.refresh(board)
        return board

    def update(self, db: Session, db_obj: Board, obj_in: dict) -> Board:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db.query(Board).filter(Board.id == id).delete()
        db.commit()


board_repository = BoardRepository()


# ====================
# TASK REPOSITORY
# ====================
class TaskRepository:
    def get(self, db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    def get_by_board(self, db: Session, board_id: int) -> List[Task]:
        return db.query(Task).filter(Task.board_id == board_id).order_by(Task.position).all()

    def get_by_status(self, db: Session, board_id: int, status: StatusEnum) -> List[Task]:
        return db.query(Task).filter(Task.board_id == board_id, Task.status == status).order_by(Task.position).all()

    def get_by_assigned_user(self, db: Session, user_id: int) -> List[Task]:
        return db.query(Task).filter(Task.assigned_to == user_id).all()

    def create(self, db: Session, obj_in: dict) -> Task:
        task = Task(**obj_in)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def update(self, db: Session, db_obj: Task, obj_in: dict) -> Task:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def move_task(self, db: Session, task_id: int, status: StatusEnum, position: Optional[int] = None) -> Task:
        task = self.get(db, task_id)
        if not task:
            return None
        task.status = status
        if position is not None:
            task.position = position
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, id: int):
        db.query(Task).filter(Task.id == id).delete()
        db.commit()


task_repository = TaskRepository()


# ====================
# TIME TRACKING REPOSITORY
# ====================
class TimeTrackingRepository:
    def get_by_task(self, db: Session, task_id: int) -> List[TimeTracking]:
        return db.query(TimeTracking).filter(TimeTracking.task_id == task_id).all()

    def get_by_user(self, db: Session, user_id: int) -> List[TimeTracking]:
        return db.query(TimeTracking).filter(TimeTracking.user_id == user_id).all()

    def create(self, db: Session, obj_in: dict) -> TimeTracking:
        entry = TimeTracking(**obj_in)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    def update(self, db: Session, db_obj: TimeTracking, obj_in: dict) -> TimeTracking:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db.query(TimeTracking).filter(TimeTracking.id == id).delete()
        db.commit()


time_tracking_repository = TimeTrackingRepository()


# ====================
# REPORT REPOSITORY
# ====================
class ReportRepository:
    def get_by_user_and_date(self, db: Session, user_id: int, date: datetime) -> Optional[Report]:
        return db.query(Report).filter(
            Report.user_id == user_id,
            func.date(Report.report_date) == date.date()
        ).first()

    def get_by_user(self, db: Session, user_id: int) -> List[Report]:
        return db.query(Report).filter(Report.user_id == user_id).all()

    def create(self, db: Session, obj_in: dict) -> Report:
        report = Report(**obj_in)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    def update(self, db: Session, db_obj: Report, obj_in: dict) -> Report:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db.query(Report).filter(Report.id == id).delete()
        db.commit()


report_repository = ReportRepository()
