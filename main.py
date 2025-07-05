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




# @app.get("/")
# async def root():
#     return {"message": "Hello, World!"}

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
#this is for hiding authentication link fro swagger


# auth_router = fastapi_users.get_auth_router(auth_backend, requires_verification=True)
# # Hide all routes from Swagger
# for route in auth_router.routes:
#     route.include_in_schema = False # type: ignore
# # Mount the modified router
# app.include_router(auth_router, prefix="/auth/jwt")


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







from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from starlette.responses import Response
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from MODELS.M_task import Task
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static",html=True),name="static")

@app.get("/")
async def home(request: Request, db: AsyncSession = Depends(get_db)) -> Response:
    result = await db.execute(select(Task))
    todos = result.scalars().all()
    return templates.TemplateResponse("auth/index.html", {"request": request, "todo_list": todos})






from fastapi import Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
#from fastapi_users import InvalidCredentialsException
#from fastapi_users.authentication import JWTAuthentication
from fastapi_users.manager import BaseUserManager
from uuid import UUID as UD
from fastapi_users.password import PasswordHelper


@app.get("/admin-login", response_class=HTMLResponse)
async def get_login_form(request: Request):
    return templates.TemplateResponse("xxx/login.html", {"request": request, "error": None})


# @app.post("/admin-login", response_class=HTMLResponse)
# async def login(
#     request: Request,
#     username: str = Form(...),
#     password: str = Form(...),
#     user_manager: BaseUserManager[UD, str] = Depends(fastapi_users.get_user_manager),
# ):
#     user = await user_manager.get_by_email(username)
#     if user is None or not user.is_superuser:
#         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

#     password_helper = PasswordHelper()
#     if not password_helper.verify(password, user.hashed_password):
#         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

#     # Create JWT token (expires in 1 hour)
#     token_data = {
#         "sub": str(user.id),
#         "aud": auth_backend.name,
#     }
#     token = generate_jwt(token_data, auth_backend.transport.secret, timedelta(hours=1))

#     response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
#     response.set_cookie(key="Authorization", value=f"Bearer {token}", httponly=True)
#     return response





