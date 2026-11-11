from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User, UserRole


class UserService:
    """
    Users ke operations handle karne ki service class.
    """

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 20) -> List[User]:
        """Tamam users ki list fetch karein (pagination ke sath)"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """User ID ke zariye specific user dhoondein"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    @staticmethod
    def update_user_role(db: Session, user_id: int, new_role: UserRole) -> User:
        """User ka role change karein (Admin only operation)"""
        user = UserService.get_user_by_id(db, user_id)
        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
