from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
import enum

from sqlalchemy import String, Boolean, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.project import Project


class UserRole(str, enum.Enum):
    """System me allowed user roles"""
    ADMIN = "admin"
    MANAGER = "manager"
    DEVELOPER = "developer"


class User(Base):
    """
    Users table - system users ki details store karta hai.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"), 
        default=UserRole.DEVELOPER, 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships (string references circular imports avoid karti hain)
    tasks: Mapped[List["Task"]] = relationship(
        "Task", 
        back_populates="assignee", 
        cascade="all, delete-orphan"
    )
    projects: Mapped[List["Project"]] = relationship(
        "Project", 
        back_populates="owner", 
        cascade="all, delete-orphan"
    )
