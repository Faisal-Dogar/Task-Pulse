import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.user_service import UserService
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate


def test_password_hashing():
    """Check password hashing & verification"""
    password = "SuperSecretPassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_user_flow():
    """Create user & verify in database"""
    db = SessionLocal()
    try:
        user = User(
            email="developer@taskpulse.com",
            hashed_password=get_password_hash("DevPass123!"),
            full_name="Dev Tester",
            role=UserRole.DEVELOPER
        )
        # Clean existing
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            db.delete(existing)
            db.commit()

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.role == UserRole.DEVELOPER

        # Test UserService
        fetched = UserService.get_user_by_id(db, user.id)
        assert fetched.email == "developer@taskpulse.com"

        # Test JWT token creation
        token = create_access_token(subject=user.id, role=user.role.value)
        assert isinstance(token, str)
        assert len(token) > 20
    finally:
        db.close()


def test_project_and_task_flow():
    """Create project, assign task, and check relationships"""
    db = SessionLocal()
    try:
        # Create test admin
        admin = db.query(User).filter(User.email == "proj_admin@taskpulse.com").first()
        if not admin:
            admin = User(
                email="proj_admin@taskpulse.com",
                hashed_password=get_password_hash("AdminPass123!"),
                full_name="Project Admin",
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        # Create project via ProjectService
        p_name = "TaskPulse Mobile App"
        old_p = db.query(Project).filter(Project.name == p_name).first()
        if old_p:
            db.delete(old_p)
            db.commit()

        project = ProjectService.create_project(
            db=db,
            project_in=ProjectCreate(name=p_name, description="Flutter app"),
            owner_id=admin.id
        )
        assert project.id is not None
        assert project.name == p_name

        # Create task via TaskService
        task = TaskService.create_task(
            db=db,
            task_in=TaskCreate(
                title="Setup Flutter SDK",
                description="Install Flutter 3.x",
                status=TaskStatus.TODO,
                priority=TaskPriority.HIGH,
                assignee_id=admin.id,
                project_id=project.id
            )
        )
        assert task.id is not None
        assert task.assignee_id == admin.id
        assert task.project_id == project.id
    finally:
        db.close()
