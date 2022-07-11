from pydantic import BaseModel, EmailStr
from datetime import datetime


class TransactionBase(BaseModel):
    amount: float
    date: str
    description: str


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionOut(TransactionBase):
    Transaction: Transaction

    class Config:
        orm_mode = True


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


class UserLogin(BaseModel):
    email: EmailStr
    password: str
