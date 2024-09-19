from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# @app.get("/")
# def read_root():
# return {"Hello World"}


class RegistrationRequest(BaseModel):
    id: int
    username: str
    emal: Union[str, None] = None
    password: str

@app.post("/registration")
async def registration(item: RegistrationRequest):
    return {
        "message": "User registered successfully"
    }

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(item: LoginRequest):
    if not all([
        len(item.password) >= 8,
        any(char.isdigit() for char in item.password),
        any(char.isupper() for char in item.password),
    ]):
        return {
            "message": "Password must be at least 8 characters, \
             contain at least one digit and one uppercase letter"
        }
    return {
        "message": "Login successful"
    }
