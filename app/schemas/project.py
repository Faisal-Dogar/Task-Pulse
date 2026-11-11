from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# 1. Base Schema: Project ki basic fields
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


# 2. Create Schema: Naya project banate waqt
class ProjectCreate(ProjectBase):
    pass


# 3. Update Schema: Project update karte waqt
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# 4. Response Schema: Client ko project ki information bhejne ke liye
class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

