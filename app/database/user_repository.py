from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import User

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


# Singleton instance để import dễ dàng
user_repository = UserRepository()
