from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.task import PriorityEnum

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.medium
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: PriorityEnum
    due_date: Optional[datetime]
    completed: bool
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True