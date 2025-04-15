from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True
