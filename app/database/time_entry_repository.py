from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database.models import TimeEntry

class TimeEntryRepository:
    def get(self, db: Session, entry_id: int) -> Optional[TimeEntry]:
        return db.query(TimeEntry).filter(TimeEntry.id == entry_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[TimeEntry]:
        return db.query(TimeEntry).offset(skip).limit(limit).all()

    def get_by_task(self, db: Session, task_id: int) -> List[TimeEntry]:
        return db.query(TimeEntry).filter(TimeEntry.task_id == task_id).order_by(TimeEntry.start_time).all()

    def get_by_user(self, db: Session, user_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[TimeEntry]:
        query = db.query(TimeEntry).filter(TimeEntry.user_id == user_id)
        if start_date:
            query = query.filter(TimeEntry.start_time >= start_date)
        if end_date:
            query = query.filter(TimeEntry.end_time <= end_date)
        return query.order_by(TimeEntry.start_time).all()

    def create(self, db: Session, obj_in: dict) -> TimeEntry:
        entry = TimeEntry(**obj_in)
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    def update(self, db: Session, db_obj: TimeEntry, obj_in: dict) -> TimeEntry:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, entry_id: int):
        db.query(TimeEntry).filter(TimeEntry.id == entry_id).delete()
        db.commit()


# Singleton instance
time_entry_repository = TimeEntryRepository()
