import typer
import asyncio
import contextlib
from sqlalchemy import select
from typing import cast
from sqlalchemy.sql import ColumnElement

from DATABASE.database import get_async_session, get_user_db
from MODELS.M_fastapi_user import UserTable
from s_users import create_user  # Your existing function

app = typer.Typer()
cli = typer.Typer()  # Main CLI app
users_cli = typer.Typer() 


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)

async def superuser_exists() -> bool:
    async with get_async_session_context() as session:
        is_superuser_column = cast(ColumnElement[bool], UserTable.is_superuser)
        result = await session.execute(
            select(UserTable).where(is_superuser_column.is_(True))
        )
        return result.scalar() is not None

@users_cli.command()
def create_superuser(
    email: str = typer.Argument(..., help="Superuser email"),
    password: str = typer.Argument(..., help="Superuser password")
):
    """Create one and only one superuser."""
    async def runner():
        if await superuser_exists():
            typer.echo("❌ Superuser already exists. Not creating another.")
        else:
            await create_user(email=email, password=password, is_superuser=True)
            typer.echo(f"✅ Superuser created: {email}")

    asyncio.run(runner())

cli.add_typer(users_cli, name="users")

if __name__ == "__main__":
    cli()
