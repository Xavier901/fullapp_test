from starlette.routing import Route
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from sqlalchemy import select, func
from DATABASE.database import AsyncSessionLocal
from MODELS.M_task import Task, UserTable
from starlette_admin.contrib.sqla import Admin

templates = Jinja2Templates(directory="templates")

class CustomAdmin(Admin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override the default dashboard route with your custom handler
        self.routes.insert(0, Route("/", endpoint=self.custom_dashboard, name="admin:dashboard"))

    async def custom_dashboard(self, request: Request) -> HTMLResponse:
        async with AsyncSessionLocal() as session:
            task_count = await session.scalar(select(func.count()).select_from(Task))
            user_count = await session.scalar(select(func.count()).select_from(UserTable))

        return templates.TemplateResponse("xxx/index.html", {
            "request": request,
            "title": "My Custom Dashboard",
            "task_count": task_count,
            "user_count": user_count
        })