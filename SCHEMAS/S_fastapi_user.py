from typing import Optional
from fastapi_users import schemas
from uuid import UUID

from pydantic import EmailStr


class UserRead(schemas.BaseUser[UUID]):
    is_superuser: bool = False
    
    model_config = {
        "from_attributes": True  # ✅ Pydantic v2 replacement for orm_mode
    }

class UserUpdate(schemas.BaseUserUpdate):
    is_superuser: Optional[bool] = None
    

# class TUserCreate(schemas.BaseUserCreate):
#     email: EmailStr
#     password: str
    
#     class Config:
#         orm_mode = True
    
class TUserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

      
class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = None
    































