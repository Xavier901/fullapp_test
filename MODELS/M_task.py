from __future__ import annotations 
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship,Mapped
# from database import  Base
from DATABASE.base import Base
from MODELS.M_fastapi_user import UserTable


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id",ondelete="CASCADE"),nullable=False)  # ✅ use "users.id"  # make sure the FK matches your user table
    #user: Mapped[Optional["UserTable"]] = relationship(back_populates="tasks") # type: ignore
    user = relationship("UserTable")
# from MODELS.M_task import Task  # ✅ import AFTER both classes exist

# UserTable.tasks = relationship("Task", back_populates="user")