from fastapi import FastAPI, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# transactions
@app.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return {"data": transactions}


@app.post("/transactions")
def create_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    new_transaction = models.Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if transaction is None:
        return {"message": "Transaction not found"}
    return transaction


@app.put("/transactions/{transaction_id}")
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


@app.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
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


# users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash passowrd
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
