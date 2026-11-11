from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, allow_admin_or_manager, allow_admin_only
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse
from app.services.project_service import ProjectService

router = APIRouter()


# 1. Tamam projects dekhne ke liye
@router.get("/", response_model=List[ProjectResponse])
def get_projects(
    skip: int = 0, 
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tamam projects fetch karein"""
    return ProjectService.get_projects(db, skip=skip, limit=limit)


# 2. Specific project dekhne ke liye
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Specific project by ID fetch karein"""
    return ProjectService.get_project_by_id(db, project_id=project_id)


# 3. Naya project banane ke liye (Sirf Admin ya Manager)
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_or_manager)
):
    """Naya project create karein (Admin/Manager only)"""
    return ProjectService.create_project(db, project_in=project_in, owner_id=current_user.id)


# 4. Project delete karne ke liye (Sirf Admin)
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_admin_only)
):
    """Project delete karein (Admin only)"""
    ProjectService.delete_project(db, project_id=project_id)
    return None
