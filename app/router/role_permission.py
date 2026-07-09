from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.rbac import require_super_admin
from app.models.role_permission import RolePermission
from app.schema.role_permission import RolePermissionCreate
from app.services import role_permission as permission_service

router = APIRouter(
    prefix="/api/role-permissions",
    tags=["role_permissions"],
)


@router.post("/")
async def save_permissions(
    payload: RolePermissionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> dict[str, str]:
    require_super_admin(current_user)

    return await permission_service.save_permissions(
        payload,
        db,
    )


@router.get("/{role_id}", response_model=None)
async def get_permissions(
    role_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> list[RolePermission]:
    require_super_admin(current_user)

    return await permission_service.get_permissions(
        role_id,
        db,
    )
