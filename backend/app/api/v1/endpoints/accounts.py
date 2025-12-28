from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User
from app.schemas.account import Account, AccountCreate, AccountUpdate

router = APIRouter()


@router.get("/", response_model=List[Account])
def read_accounts(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Get all accounts for current user."""
    accounts = crud.account.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return accounts


@router.post("/", response_model=Account, status_code=status.HTTP_201_CREATED)
def create_account(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    account_in: AccountCreate,
) -> Any:
    """Create new account."""
    account = crud.account.create_with_user(
        db, obj_in=account_in, user_id=current_user.id
    )
    return account


@router.get("/{account_id}", response_model=Account)
def read_account(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    account_id: int,
) -> Any:
    """Get account by ID."""
    account = crud.account.get_user_account(
        db, account_id=account_id, user_id=current_user.id
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    return account


@router.put("/{account_id}", response_model=Account)
def update_account(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    account_id: int,
    account_in: AccountUpdate,
) -> Any:
    """Update account."""
    account = crud.account.get_user_account(
        db, account_id=account_id, user_id=current_user.id
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    account = crud.account.update(db, db_obj=account, obj_in=account_in)
    return account


@router.delete("/{account_id}")
def delete_account(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    account_id: int,
) -> Any:
    """Delete account."""
    account = crud.account.get_user_account(
        db, account_id=account_id, user_id=current_user.id
    )
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    crud.account.delete(db, id=account_id)
    return {"message": "Account deleted successfully"}
