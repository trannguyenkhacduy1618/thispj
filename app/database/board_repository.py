from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import Board

class BoardRepository:
    def get(self, db: Session, board_id: int) -> Optional[Board]:
        return db.query(Board).filter(Board.id == board_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Board]:
        return db.query(Board).offset(skip).limit(limit).all()

    def get_by_owner(self, db: Session, owner_id: int) -> List[Board]:
        return db.query(Board).filter(Board.owner_id == owner_id).all()

    def get_accessible_boards(self, db: Session, user_id: int) -> List[Board]:
        """
        Boards owned by user + public boards
        """
        return db.query(Board).filter(
            (Board.owner_id == user_id) | (Board.is_public == True)
        ).all()

    def get_public_boards(self, db: Session) -> List[Board]:
        return db.query(Board).filter(Board.is_public == True).all()

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


# Singleton instance
board_repository = BoardRepository()
