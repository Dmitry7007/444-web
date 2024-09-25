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
