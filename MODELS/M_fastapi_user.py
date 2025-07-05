from __future__ import annotations 
from typing import List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship,Mapped
#locals
from DATABASE.base import Base
  # Import Task model to establish relationship



class UserTable(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    first_name = Column(String, nullable=True, default="first name")
    last_name = Column(String, nullable=True, default="lastname")
    profile_pic = Column(String, nullable=True)  # Change this to your actual default image path or URL
    phone_number = Column(String, nullable=True, default="+919999999999")
    
    
    #tasks: Mapped[List["Task"]] = relationship(back_populates="user") # type: ignore
    #tasks = relationship("Task", back_populates="user")
    #profile_pic = Column(String, nullable=True, default="default_profile.png")



# from MODELS.M_task import Task  # ✅ Delayed import after Task is defined

# UserTable.tasks = relationship("Task", back_populates="user")










