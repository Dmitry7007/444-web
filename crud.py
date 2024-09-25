from sqlalchemy.orm import Session
from . import models, schemas

def registration(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, 
        username=user.username, 
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id( db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email( db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_active_users(db: Session):
    return db.query(models.User).filter(models.User.is_active == True).all()
