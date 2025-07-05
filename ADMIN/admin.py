from DATABASE.database import engine
from starlette_admin.contrib.sqla import Admin,ModelView

from MODELS.M_task import Task,UserTable



admin=Admin(
    engine=engine,
    title="Task Admin",
    route_name="admin"
)


admin.add_view(ModelView(Task,icon="fa fa-tasks"))
admin.add_view(ModelView(UserTable, icon="fa fa-user", label="Users"))
