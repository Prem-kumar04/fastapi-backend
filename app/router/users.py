from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.rbac import require_admin_or_super_admin, require_super_admin
from app.schema.user import ProfileUpdate, UserCreate, UserUpdate
from app.services import user as user_service

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

USER_NOT_FOUND = "User not found"


@router.get(
    "/me",
    responses={
        404: {
            "description": USER_NOT_FOUND,
        },
    },
)
async def get_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, Any]:
    user = await user_service.get_user_by_id(
        current_user["user_id"],
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_FOUND,
        )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }


@router.put(
    "/me",
    responses={
        404: {
            "description": USER_NOT_FOUND,
        },
    },
)
async def update_my_profile(
    payload: ProfileUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    user = await user_service.get_user_by_id(
        current_user["user_id"],
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_FOUND,
        )

    return await user_service.update_profile(
        user,
        payload,
        db,
    )


@router.get("/")
async def get_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> list[dict[str, Any]]:
    require_admin_or_super_admin(current_user)

    return await user_service.get_users(db)


@router.post("/")
async def create_user(
    payload: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Any:
    require_super_admin(current_user)

    return await user_service.create_user(
        payload,
        db,
    )


@router.put(
    "/{user_id}",
    responses={
        404: {
            "description": USER_NOT_FOUND,
        },
    },
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> Any:
    require_super_admin(current_user)

    user = await user_service.get_user_by_id(
        user_id,
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_FOUND,
        )

    return await user_service.update_user(
        user,
        payload,
        db,
    )


@router.delete(
    "/{user_id}",
    responses={
        404: {
            "description": USER_NOT_FOUND,
        },
    },
)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, str]:
    require_super_admin(current_user)

    user = await user_service.get_user_by_id(
        user_id,
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=USER_NOT_FOUND,
        )

    return await user_service.delete_user(
        user,
        db,
    )
