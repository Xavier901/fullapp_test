from fastapi import Depends, HTTPException, status
from AUTHENTICATION.auth import fastapi_users
from MODELS.M_fastapi_user import UserTable as User

async def require_active_user(user: User = Depends(fastapi_users.current_user(active=True))):
    return user

async def require_superuser(user: User = Depends(fastapi_users.current_user(active=True))):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Superuser access required")
    return user
