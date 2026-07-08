from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_permission import RolePermission


async def save_permissions(
    payload: Any,
    db: AsyncSession,
) -> dict[str, str]:
    await db.execute(
        delete(RolePermission).where(
            RolePermission.role_id == payload.role_id
        )
    )

    for item in payload.permissions:
        permission = RolePermission(
            role_id=payload.role_id,
            module_id=item.module_id,
            can_view=item.can_view,
            can_create=item.can_create,
            can_edit=item.can_edit,
            can_delete=item.can_delete,
        )

        db.add(permission)

    await db.commit()

    return {
        "message": "Permissions saved successfully",
    }


async def get_permissions(
    role_id: int,
    db: AsyncSession,
) -> list[RolePermission]:
    result = await db.execute(
        select(RolePermission).where(
            RolePermission.role_id == role_id
        )
    )

    return list(result.scalars().all())
