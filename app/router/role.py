from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.schema.role import RoleCreate, RoleResponse, RoleUpdate
from app.services import role as role_service

ROLE_NOT_FOUND = "Role not found"

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
)


@router.get("/")
async def get_roles(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> list[RoleResponse]:
    roles = await role_service.get_roles(db)
    return [RoleResponse.model_validate(role) for role in roles]


@router.post("/")
async def create_role(
    payload: RoleCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> RoleResponse:
    role = await role_service.create_role(payload, db)
    return RoleResponse.model_validate(role)


@router.put(
    "/{role_id}",
    responses={
        404: {
            "description": ROLE_NOT_FOUND,
        },
    },
)
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> RoleResponse:
    role = await role_service.get_role_by_id(role_id, db)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail=ROLE_NOT_FOUND,
        )

    updated_role = await role_service.update_role(
        role,
        payload,
        db,
    )

    return RoleResponse.model_validate(updated_role)


@router.delete(
    "/{role_id}",
    responses={
        404: {
            "description": ROLE_NOT_FOUND,
        },
    },
)
async def delete_role(
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> dict[str, str]:
    role = await role_service.get_role_by_id(role_id, db)

    if role is None:
        raise HTTPException(
            status_code=404,
            detail=ROLE_NOT_FOUND,
        )

    return await role_service.delete_role(
        role,
        db,
    )
