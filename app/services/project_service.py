from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.project import Project
from app.schemas.project import ProjectCreate


class ProjectService:
    """
    Projects ke operations handle karne ki service class.
    """

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 20) -> List[Project]:
        """Tamam projects fetch karein"""
        return db.query(Project).offset(skip).limit(limit).all()

    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> Project:
        """ID se specific project dhoondein"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project

    @staticmethod
    def create_project(db: Session, project_in: ProjectCreate, owner_id: int) -> Project:
        """Naya project create karein (check duplicate name)"""
        existing = db.query(Project).filter(Project.name == project_in.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name already exists"
            )

        db_project = Project(
            name=project_in.name,
            description=project_in.description,
            owner_id=owner_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> None:
        """Project delete karein"""
        project = ProjectService.get_project_by_id(db, project_id)
        db.delete(project)
        db.commit()
