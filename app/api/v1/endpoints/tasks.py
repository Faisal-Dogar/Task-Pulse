from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_db,
    get_current_user,
    allow_admin_or_manager,
    allow_admin_only,
)
from app.models.task import TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


# 1. Tasks list fetch karein
@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    project_id: Optional[int] = Query(None, alias="project_id"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Tasks list fetch karein:
    - Developers sirf apne tasks dekh sakte hain
    - Admin/Manager sabhi tasks dekh sakte hain
    """
    return TaskService.get_tasks(
        db=db,
        current_user=current_user,
        status_filter=status_filter,
        project_id=project_id,
        skip=skip,
        limit=limit,
    )


# 2. Specific task details
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Specific task by ID fetch karein"""
    return TaskService.get_task_by_id(db, task_id=task_id)


# 3. Naya task create karein (Sirf Admin ya Manager)
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_or_manager),
):
    """Naya task banayein (Admin / Manager only)"""
    return TaskService.create_task(db=db, task_in=task_in)


# 4. Task update karein (Developer apna task update kar sakta hai, Admin/Manager koi bhi)
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Task update karein (status, priority waghera)"""
    return TaskService.update_task(
        db=db, 
        task_id=task_id, 
        task_in=task_in, 
        current_user=current_user
    )


# 5. Task delete karein (Sirf Admin)
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_only),
):
    """Task delete karein (Sirf Admin)"""
    TaskService.delete_task(db=db, task_id=task_id)
    return None
