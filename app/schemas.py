from pydantic import BaseModel, EmailStr
from datetime import datetime


class TransactionBase(BaseModel):
    amount: float
    date: str
    description: str


class TransactionCreate(TransactionBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
