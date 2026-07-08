from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.schema.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task as task_service

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=TaskResponse)
async def create_task(
    payload: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> TaskResponse:
    print("CURRENT USER =", current_user)

    task = await task_service.create_task(
        payload,
        db,
    )

    return TaskResponse.model_validate(task)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[TaskResponse]:
    tasks = await task_service.get_tasks(db)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        404: {
            "description": "Task not found",
        },
    },
)
async def get_task_by_id(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> TaskResponse:
    task = await task_service.get_task_by_id(
        task_id,
        db,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    responses={
        404: {
            "description": "Task not found",
        },
    },
)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> TaskResponse:
    task = await task_service.get_task_by_id(
        task_id,
        db,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    updated_task = await task_service.update_task(
        task,
        payload,
        db,
    )

    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{task_id}",
    responses={
        404: {
            "description": "Task not found",
        },
    },
)
async def delete_task(
    task_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    print("CURRENT USER =", current_user)

    task = await task_service.get_task_by_id(
        task_id,
        db,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return await task_service.delete_task(
        task,
        db,
    )
