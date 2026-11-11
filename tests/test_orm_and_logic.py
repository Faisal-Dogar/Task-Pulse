import sys
from pathlib import Path

# Add project root to sys.path so 'import app' always works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.models.project import Project
from app.models.task import Task, TaskStatus, TaskPriority
from app.core.security import get_password_hash, verify_password, create_access_token


def test_everything():
    db = SessionLocal()
    try:
        # 1. Test password hashing
        pwd = "SecretPassword123!"
        hashed = get_password_hash(pwd)
        assert verify_password(pwd, hashed) is True
        print("✓ Password hashing & verification OK")

        # 2. Clear old test data
        db.query(Task).delete()
        db.query(Project).delete()
        db.query(User).delete()
        db.commit()

        # 3. Test user creation
        user = User(
            email="admin@taskpulse.com",
            hashed_password=hashed,
            full_name="Admin User",
            role=UserRole.ADMIN
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        assert user.id is not None
        print(f"✓ User created with ID: {user.id}")

        # 4. Test token generation
        token = create_access_token(subject=user.id, role=user.role.value)
        assert token is not None
        print("✓ JWT access token generation OK")

        # 5. Test project creation
        project = Project(
            name="Website Redesign",
            description="Redesign the landing page and dashboard",
            owner_id=user.id
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        assert project.id is not None
        print(f"✓ Project created with ID: {project.id}")

        # 6. Test task creation
        task = Task(
            title="Design Home Hero Section",
            description="Use Figma for hero layout",
            status=TaskStatus.TODO,
            priority=TaskPriority.HIGH,
            assignee_id=user.id,
            project_id=project.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        assert task.id is not None
        print(f"✓ Task created with ID: {task.id}")

        # 7. Verify ORM relationships
        assert task.assignee.email == "admin@taskpulse.com"
        assert task.project.name == "Website Redesign"
        assert len(project.tasks) == 1
        assert len(user.projects) == 1
        assert len(user.tasks) == 1
        print("✓ All ORM Relationships & Foreign Keys OK")

        print("\nAll database models, security, and relationships passed successfully!")
    finally:
        db.close()


if __name__ == "__main__":
    test_everything()
