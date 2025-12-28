from typing import Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate

router = APIRouter()


@router.get("/", response_model=List[Transaction])
def read_transactions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    account_id: Optional[int] = None,
    category_id: Optional[int] = None,
) -> Any:
    """Get all transactions for current user with optional filters."""
    transactions = crud.transaction.get_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        account_id=account_id,
        category_id=category_id,
    )
    return transactions


@router.post("/", response_model=Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    transaction_in: TransactionCreate,
) -> Any:
    """Create new transaction."""
    try:
        transaction = crud.transaction.create_with_user(
            db, obj_in=transaction_in, user_id=current_user.id
        )
        return transaction
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get("/{transaction_id}", response_model=Transaction)
def read_transaction(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    transaction_id: int,
) -> Any:
    """Get transaction by ID."""
    transaction = crud.transaction.get_user_transaction(
        db, transaction_id=transaction_id, user_id=current_user.id
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    transaction_id: int,
    transaction_in: TransactionUpdate,
) -> Any:
    """Update transaction."""
    transaction = crud.transaction.get_user_transaction(
        db, transaction_id=transaction_id, user_id=current_user.id
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    transaction = crud.transaction.update(
        db, db_obj=transaction, obj_in=transaction_in
    )
    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    transaction_id: int,
) -> Any:
    """Delete transaction."""
    transaction = crud.transaction.get_user_transaction(
        db, transaction_id=transaction_id, user_id=current_user.id
    )
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    crud.transaction.delete(db, id=transaction_id)
    return {"message": "Transaction deleted successfully"}
