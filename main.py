from fastapi import FastAPI,Depends, HTTPException, status




#LOCAL
from DATABASE.database import get_async_session, AsyncSessionLocal,engine,get_db
from DATABASE.base import Base
from AUTHENTICATION.auth import fastapi_users,auth_backend
from SCHEMAS.S_fastapi_user import UserRead, UserUpdate, UserCreate,TUserCreate
from AUTHENTICATION.user_manager import get_user_manager
from fastapi_users.exceptions import UserAlreadyExists
from APP import task_r
from ADMIN.admin import admin
app = FastAPI()




app.include_router(task_r.task_router,prefix="/Task")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


admin.mount_to(app)




@app.get("/")
async def root():
    return {"message": "Hello, World!"}

#user update ,get 
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate,True),  # ✅ provide schemas
    prefix="/users",
    tags=["users"]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend,True),  # ✅ no [0]
    prefix="/auth/jwt",
    tags=["auth"]
)

#token base varification
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)

#user create 
# app.include_router(
#     fastapi_users.get_register_router(UserRead, TUserCreate),
#     prefix="/auth",
#     tags=["auth"]
# )

@app.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_create: TUserCreate, user_manager=Depends(get_user_manager)):
    try:
        if user_create.is_superuser == True:
            raise HTTPException(status_code=404,detail="Super user can't be created.")
        else:
            user = await user_manager.create(user_create)
        return user
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="User already exists")























