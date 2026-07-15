from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.user import User
from app.models.user_permission import UserPermission
from app.schema.user import ProfileUpdate, UserCreate, UserUpdate


async def create_user(
    payload: UserCreate,
    db: AsyncSession,
) -> dict[str, Any]:
    # Find or create role
    role_result = await db.execute(
        select(Role).where(Role.name == payload.role_name)
    )
    role = role_result.scalar_one_or_none()

    if role is None:
        role = Role(
            name=payload.role_name,
            description=f"{payload.role_name} Role",
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)

    role_name = role.name

    user = User(
        username=payload.username,
        slug=payload.username.lower(),
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        password=payload.password,
        role_id=role.id,
    )

    db.add(user)
    await db.flush()

    user_id = user.id
    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    await db.commit()

    if payload.permissions:
        for module, perms in payload.permissions.items():
            user_perm = UserPermission(
                user_id=user_id,
                module=module,
                view=perms.view,
                create=perms.create,
                edit=perms.edit,
                delete=perms.delete,
                export=perms.export,
            )
            db.add(user_perm)

        await db.commit()

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "role_name": role_name,
    }
    


async def get_user_permissions(
    user_id: int,
    db: AsyncSession,
) -> dict[str, dict[str, bool]]:
    result = await db.execute(
        select(UserPermission).where(
            UserPermission.user_id == user_id
        )
    )

    rows = result.scalars().all()

    permissions: dict[str, dict[str, bool]] = {}

    for perm in rows:
        permissions[perm.module] = {
            "view": perm.view,
            "create": perm.create,
            "edit": perm.edit,
            "delete": perm.delete,
            "export": perm.export,
        }

    return permissions


async def get_user_by_email(
    email: str,
    db: AsyncSession,
) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()


async def get_users(
    db: AsyncSession,
) -> list[dict[str, Any]]:
    result = await db.execute(
        select(User, Role).outerjoin(
            Role,
            User.role_id == Role.id,
        )
    )

    rows = result.all()

    users: list[dict[str, Any]] = []

    for user, role in rows:
        users.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": role.name if role else "",
            }
        )

    return users


async def get_user_by_id(
    user_id: int,
    db: AsyncSession,
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()


async def update_user(
    user: User,
    payload: UserUpdate,
    db: AsyncSession,
) -> dict[str, Any]:
    role_result = await db.execute(
        select(Role).where(Role.name == payload.role_name)
    )
    role = role_result.scalar_one_or_none()

    if role is None:
        role = Role(
            name=payload.role_name,
            description=f"{payload.role_name} Role",
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)

    role_name = role.name

    user.username = payload.username
    user.slug = payload.username.lower()
    user.email = payload.email
    user.first_name = payload.first_name
    user.last_name = payload.last_name
    user.role_id = role.id

    await db.flush()

    user_id = user.id
    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    await db.commit()

    if payload.permissions:
        await db.execute(
            delete(UserPermission).where(
                UserPermission.user_id == user_id
            )
        )

        for module, perms in payload.permissions.items():
            db.add(
                UserPermission(
                    user_id=user_id,
                    module=module,
                    view=perms.view,
                    create=perms.create,
                    edit=perms.edit,
                    delete=perms.delete,
                    export=perms.export,
                )
            )

        await db.commit()

    return {
        "id": user_id,
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "role_name": role_name,
    }


async def update_profile(
    user: User,
    payload: ProfileUpdate,
    db: AsyncSession,
) -> dict[str, str]:
    user.first_name = payload.first_name
    user.last_name = payload.last_name

    if payload.password and payload.password.strip():
        user.password = payload.password

    await db.commit()
    await db.refresh(user)

    return {
        "message": "Profile updated successfully",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
    }


async def delete_user(
    user: User,
    db: AsyncSession,
) -> dict[str, str]:
    await db.execute(
        delete(UserPermission).where(
            UserPermission.user_id == user.id
        )
    )

    await db.delete(user)
    await db.commit()

    return {
        "message": "User deleted successfully",
    }
