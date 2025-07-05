from pydantic import BaseModel, EmailStr
from typing import Optional

from SCHEMAS.S_fastapi_user import UserRead  # Import the User model for type hinting
from uuid import UUID


class TaskBase(BaseModel):
    name: str
    description: str

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    #user:UserRead
    user: Optional[UserRead] = None 
    user_id:UUID
    class Config:
        orm_mode = True
        