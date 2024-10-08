from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class WalletCreate(BaseModel):
    user_id: int
    personal_account: int

class UserLogin(BaseModel):
    email: str
    password: str