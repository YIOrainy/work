from db import User
from services.auth.auth_utils import getPasswordHash
from services.user.DTO.user_dto import UserCreate, UserResponse
from sqlalchemy.orm import Session

def getUserByEmail(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def createUser(user_data: UserCreate, db: Session):
    # Check if user already exists
    if getUserByEmail(user_data.email, db):
        return None
    
    db_user = User(
        email=user_data.email,
        password=getPasswordHash(user_data.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user