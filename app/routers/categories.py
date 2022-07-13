from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

# categories
@router.get("/", response_model=List[schemas.Category])
def get_categories(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    # limit: int = 10,
    # offset: int = 0,
    # search: Optional[str] = None
):
    categories = (
        db.query(models.Category).filter(models.Category.owner_id == current_user.id)
        # .limit(limit)
        # .offset(offset)
        .all()
    )
    return categories


@router.post("/")
def create_transaction(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_category = models.Category(owner_id=current_user.id, **category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# @router.get("/{transaction_id}", response_model=schemas.category)
# def get_category(
#     transaction_id: int,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     category = (
#         db.query(models.category)
#         .filter(models.category.id == transaction_id)
#         .first()
#     )
#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="category not found"
#         )

#     if category.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
#         )
#     return category


# @router.put("/{transaction_id}", response_model=schemas.category)
# def update_category(
#     transaction_id: int,
#     updated_transaction: schemas.TransactionCreate,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     transaction_query = db.query(models.category).filter(
#         models.category.id == transaction_id
#     )

#     category = transaction_query.first()

#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="category not found"
#         )
#     if category.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
#         )

#     transaction_query.update(updated_transaction.dict(), synchronize_session=False)
#     db.commit()

#     return transaction_query.first()


# @router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(
#     transaction_id: int,
#     db: Session = Depends(get_db),
#     current_user: int = Depends(oauth2.get_current_user),
# ):

#     transaction_query = db.query(models.category).filter(
#         models.category.id == transaction_id
#     )

#     category = transaction_query.first()

#     if category is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="category not found"
#         )
#     if category.owner_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
#         )

#     transaction_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
