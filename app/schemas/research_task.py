from pydantic import BaseModel

class TaskBase(BaseModel):
    project_id: int
    title: str
    description: str | None = None
    assignee_id: int
    status: str
    priority: str
    due_date: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True