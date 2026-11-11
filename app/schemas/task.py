from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.task import TaskStatus, TaskPriority
from app.schemas.user import UserResponse


# 1. Base Schema: Task ki common fields
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None


# 2. Create Schema: Naya task create karne ke liye
class TaskCreate(TaskBase):
    pass


# 3. Update Schema: Task ki fields update karne ke liye
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    project_id: Optional[int] = None


# 4. Response Schema: Client ko task data return karne ke liye
class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # Assigned user ki details (agar task kisi user ko assign hai)
    assignee: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
