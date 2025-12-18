from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.session import SessionLocal
from app.database import user_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")




def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()




def get_current_user(
token: str = Depends(oauth2_scheme),
db: Session = Depends(get_db)
):
credentials_exception = HTTPException(
status_code=status.HTTP_401_UNAUTHORIZED,
detail="Could not validate credentials",
headers={"WWW-Authenticate": "Bearer"},
)


try:
payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
user_id: str = payload.get("sub")
if user_id is None:
raise credentials_exception
except JWTError:
raise credentials_exception


user = user_repository.get_by_id(db, int(user_id))
if not user or not user.is_active:
raise credentials_exception


return user




def require_admin(current_user=Depends(get_current_user)):
if current_user.role != "admin":
raise HTTPException(
status_code=status.HTTP_403_FORBIDDEN,
detail="Admin privileges required"
)
return current_user
