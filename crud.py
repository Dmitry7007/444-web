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

def get_wallet_by_user(db: Session, user_id: int):
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

def get_wallet_by_id(db: Session, wallet_id: int):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

def get_wallet_by_user_id(db: Session, user_id: int):
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

def create_wallet(db: Session, wallet: schemas.WalletCreate):
    db_wallet = models.Wallet(
        user_id=wallet.user_id, 
        personal_account=wallet.personal_account
        )
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password