from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.schema.role import RoleCreate, RoleResponse, RoleUpdate
from app.services import role as role_service

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
)


@router.get("/", response_model=list[RoleResponse])
async def get_roles(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[RoleResponse]:
    roles = await role_service.get_roles(db)
    return [RoleResponse.model_validate(role) for role in roles]


@router.post("/", response_model=RoleResponse)
async def create_role(
    payload: RoleCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> RoleResponse:
    role = await role_service.create_role(payload, db)
    return RoleResponse.model_validate(role)


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> RoleResponse:
    role = await role_service.get_role_by_id(role_id, db)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    updated_role = await role_service.update_role(role, payload, db)
    return RoleResponse.model_validate(updated_role)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    role = await role_service.get_role_by_id(role_id, db)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return await role_service.delete_role(role, db)
