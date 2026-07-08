from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schema.task import TaskCreate, TaskUpdate


async def create_task(
    payload: TaskCreate,
    db: AsyncSession,
) -> Task:
    task = Task(
        title=payload.title,
        description=payload.description,
        assigned_employee_id=payload.assigned_employee_id,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def get_tasks(
    db: AsyncSession,
) -> list[Task]:
    result = await db.execute(
        select(Task)
    )

    return list(result.scalars().all())


async def get_task_by_id(
    task_id: int,
    db: AsyncSession,
) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )

    return result.scalar_one_or_none()


async def update_task(
    task: Task,
    payload: TaskUpdate,
    db: AsyncSession,
) -> Task:
    task.title = payload.title
    task.description = payload.description
    task.status = payload.status
    task.assigned_employee_id = payload.assigned_employee_id

    await db.commit()
    await db.refresh(task)

    return task


async def delete_task(
    task: Task,
    db: AsyncSession,
) -> dict[str, str]:
    await db.delete(task)
    await db.commit()

    return {
        "message": "Task deleted successfully",
    }
