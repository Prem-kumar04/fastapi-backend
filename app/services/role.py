from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.role_permission import RolePermission
from app.schema.role import RoleCreate, RoleUpdate


async def create_role(
    payload: RoleCreate,
    db: AsyncSession,
) -> Role:
    role = Role(
        name=payload.name,
        description=payload.description,
    )

    db.add(role)
    await db.commit()
    await db.refresh(role)

    if payload.permissions:
        for permission in payload.permissions:
            role_permission = RolePermission(
                role_id=role.id,
                module_id=permission.module_id,
                can_view=permission.can_view,
                can_create=permission.can_create,
                can_edit=permission.can_edit,
                can_delete=permission.can_delete,
            )
            db.add(role_permission)

        await db.commit()

    return role


async def get_roles(
    db: AsyncSession,
) -> list[Role]:
    result = await db.execute(select(Role))

    return list(result.scalars().all())


async def get_role_by_id(
    role_id: int,
    db: AsyncSession,
) -> Role | None:
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )

    return result.scalar_one_or_none()


async def update_role(
    role: Role,
    payload: RoleUpdate,
    db: AsyncSession,
) -> Role:
    role.name = payload.name
    role.description = payload.description

    if payload.permissions is not None:
        await db.execute(
            delete(RolePermission).where(
                RolePermission.role_id == role.id
            )
        )

        for permission in payload.permissions:
            role_permission = RolePermission(
                role_id=role.id,
                module_id=permission.module_id,
                can_view=permission.can_view,
                can_create=permission.can_create,
                can_edit=permission.can_edit,
                can_delete=permission.can_delete,
            )

            db.add(role_permission)

    await db.commit()
    await db.refresh(role)

    return role


async def delete_role(
    role: Role,
    db: AsyncSession,
) -> dict[str, str]:
    await db.execute(
        delete(RolePermission).where(
            RolePermission.role_id == role.id
        )
    )

    await db.delete(role)
    await db.commit()

    return {
        "message": "Role deleted successfully",
    }
