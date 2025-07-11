from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.models import User

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    if not token.isdigit():
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(token)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user
