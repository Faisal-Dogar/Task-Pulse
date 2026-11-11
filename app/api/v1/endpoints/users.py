from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, allow_admin_only
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.services.user_service import UserService

router = APIRouter()


# 1. Logged-in user ki profile
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Current logged-in user ki details dekhein"""
    return current_user


# 2. Tamam users ki list (Authentication zaroori hai)
@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0, 
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tamam registered users dekhne ke liye"""
    return UserService.get_users(db, skip=skip, limit=limit)


# 3. User ka role change karein (Sirf Admin kar sakta hai)
@router.patch("/{user_id}/role", response_model=UserResponse)
def change_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_only)
):
    """User ka role change karein (Sirf Admin)"""
    return UserService.update_user_role(db, user_id=user_id, new_role=new_role)
