from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload


from SCHEMAS import S_task
from DATABASE.database import get_db,AsyncSession
from MODELS.M_task import Task
from MODELS.M_fastapi_user import UserTable
from AUTHENTICATION.auth import current_active_user


task_router=APIRouter()


# @task_router.post("/items/", response_model=S_task.Task)
# async def create_task(
#     item: S_task.TaskCreate,
#     db: AsyncSession = Depends(get_db),
#     user: UserTable = Depends(current_active_user)  # 🔐 Require login
# ):
#     db_item = M_task.Task(**item.dict(), user_id=user.id)  # Link task to user
#     db.add(db_item)
#     await db.commit()
#     await db.refresh(db_item)
#     return db_item

@task_router.post("/items/", response_model=S_task.Task)
async def create_task(
    item: S_task.TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: UserTable = Depends(current_active_user)
):
    db_item = Task(**item.dict(), user_id=user.id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    # Eager load user relationship explicitly
    result = await db.execute(
        select(Task)
        .options(selectinload(Task.user))
        .where(Task.id == db_item.id)
    )
    db_item_with_user = result.scalars().first()

    return db_item_with_user


@task_router.get("/items/", response_model=list[S_task.Task])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(current_active_user),
):
    if current_user.is_superuser:
        query = select(Task).options(selectinload(Task.user)).offset(skip).limit(limit) # ❌ no need to join user
    else:
        query = (
            select(Task)
            .where(Task.user_id == current_user.id)
            .options(selectinload(Task.user))
            .offset(skip)
            .limit(limit) )
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@task_router.get("/items/{item_id}", response_model=S_task.Task)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(current_active_user),
):
    result = await db.execute(
        select(Task)
        .where(Task.id == item_id)
        .options(selectinload(Task.user))  # ✅ eagerly load relationship
    )
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if not current_user.is_superuser and item.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not authorized")

    return item  # ✅ now safe: FastAPI can serialize `item.user`


@task_router.put("/items/{item_id}", response_model=S_task.Task)
async def update_item(
    item_id: int,
    item: S_task.TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(current_active_user),
):
    # Eagerly load the item and its user
    result = await db.execute(
        select(Task)
        .where(Task.id == item_id)
        .options(selectinload(Task.user))
    )
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Authorization check
    if not current_user.is_superuser and db_item.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not authorized to update this item")

    # Update fields
    for key, value in item.dict().items():
        setattr(db_item, key, value)

    await db.commit()
    await db.refresh(db_item)
    return db_item


@task_router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserTable = Depends(current_active_user),
):
    # Eagerly load the item and its user
    result = await db.execute(
        select(Task)
        .where(Task.id == item_id)
        .options(selectinload(Task.user))
    )
    db_item = result.scalar_one_or_none()

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Authorization: only allow if user owns the item or is superuser
    if not current_user.is_superuser and db_item.user_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    await db.delete(db_item)
    await db.commit()
    return {"detail": "Item deleted"}
















