from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task import Task, TaskStatus
from app.models.user import User, UserRole
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """
    Tasks ke business logic operations handle karne ki service class.
    """

    @staticmethod
    def get_tasks(
        db: Session,
        current_user: User,
        status_filter: Optional[TaskStatus] = None,
        project_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Task]:
        """
        Tasks list fetch karein:
        - Developer sirf apne assigned tasks dekh sakta hai
        - Admin aur Manager sabhi tasks dekh sakte hain
        """
        query = db.query(Task)

        # Developer filter
        if current_user.role == UserRole.DEVELOPER:
            query = query.filter(Task.assignee_id == current_user.id)

        # Optional filters
        if status_filter:
            query = query.filter(Task.status == status_filter)
        if project_id:
            query = query.filter(Task.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int) -> Task:
        """ID se specific task dhoondein"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task

    @staticmethod
    def create_task(db: Session, task_in: TaskCreate) -> Task:
        """Naya task database me save karein"""
        db_task = Task(**task_in.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task(
        db: Session,
        task_id: int,
        task_in: TaskUpdate,
        current_user: User,
    ) -> Task:
        """
        Task update karein:
        - Developer sirf apna assigned task update kar sakta hai
        - Admin aur Manager koi bhi task update kar sakte hain
        """
        task = TaskService.get_task_by_id(db, task_id)

        # Permission check
        if current_user.role == UserRole.DEVELOPER and task.assignee_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own assigned tasks"
            )

        # Sirf wahi fields update hongi jo user ne provide ki hain
        update_data = task_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> None:
        """Task delete karein (Sirf Admin)"""
        task = TaskService.get_task_by_id(db, task_id)
        db.delete(task)
        db.commit()
