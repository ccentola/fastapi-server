from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from typing import List
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import engine, get_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# transactions
@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return transactions


@router.post("/")
def create_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    new_transaction = models.Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if transaction is None:
        return {"message": "Transaction not found"}
    return transaction


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    updated_transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    transaction_query = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    )

    transaction = transaction_query.first()

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    transaction_query.update(updated_transaction.dict(), synchronize_session=False)
    db.commit()

    return {"data": transaction_query.first()}


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    )
    if transaction.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    transaction.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
