from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import Task, StatusEnum

class TaskRepository:
    def get(self, db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(Task).offset(skip).limit(limit).all()

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

    def delete(self, db: Session, id: int):
        db.query(Task).filter(Task.id == id).delete()
        db.commit()

    def move_task(self, db: Session, task_id: int, new_status: StatusEnum, new_position: Optional[int] = None) -> Task:
        task = self.get(db, task_id)
        if not task:
            return None

        # Nếu status thay đổi, lấy số lượng tasks hiện tại của status mới
        if task.status != new_status:
            task.status = new_status
            tasks_in_new_status = db.query(Task).filter(Task.board_id == task.board_id, Task.status == new_status).order_by(Task.position).all()
            task.position = new_position if new_position is not None else len(tasks_in_new_status)
        else:
            if new_position is not None:
                task.position = new_position

        db.commit()
        db.refresh(task)
        return task


# Singleton instance
task_repository = TaskRepository()
