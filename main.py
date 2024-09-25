from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine
import models, schemas, crud
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/registration", response_model=schemas.User)
def registration(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not user.username:
        raise HTTPException(status_code=400, detail="Username is required")
    if not user.email:
        raise HTTPException(status_code=400, detail="Email is required")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.registration(db=db, user=user)


@app.post("/login", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not crud.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return db_user

@app.post("/wallet", response_model=schemas.WalletCreate)
def create_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_db)):
    return crud.create_wallet(db=db, wallet=wallet)