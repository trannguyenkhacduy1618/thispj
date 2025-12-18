from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo engine
engine = create_engine(
    settings.DATABASE_URL,   # dùng đúng tên biến trong Settings
    pool_pre_ping=True,
    future=True,  # SQLAlchemy 2.0 style
)

# Tạo SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Dependency để lấy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()