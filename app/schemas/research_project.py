from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: str | None = None
    owner_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MemberBase(BaseModel):
    project_id: int
    user_id: int
    role: str

class MemberCreate(MemberBase):
    pass

class MemberResponse(MemberBase):
    joined_at: datetime

    class Config:
        from_attributes = True