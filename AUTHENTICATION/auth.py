from uuid import UUID
import os
from fastapi_users import FastAPIUsers
#from fastapi_users.authentication import JWTAuthentication
from fastapi_users.authentication import (
    AuthenticationBackend,BearerTransport,JWTStrategy,)

from AUTHENTICATION.user_manager import get_user_manager # type: ignore
from MODELS.M_fastapi_user import UserTable

SECRET = os.getenv("SECRET")  # use env var

# 1. Define the transport (how the token is sent)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# 2. Define the strategy (how the token is created/verified)
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600) # type: ignore

# 3. Combine them into an authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

#auth_backends = [JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login")]

fastapi_users = FastAPIUsers[UserTable, UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)







