from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class TransactionBase(BaseModel):
    amount: float
    date: str
    description: str


class Transaction(TransactionBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class TransactionOut(TransactionBase):
    Transaction: Transaction

    class Config:
        orm_mode = True


class TransactionCreate(TransactionBase):
    pass


class CategoryBase(BaseModel):
    category: str


class Category(CategoryBase):
    id: int
    category: str
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass
