from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: float
    date: str
    description: str


class TransactionCreate(TransactionBase):
    pass
