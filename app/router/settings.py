from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.rbac import require_super_admin
from app.schema.settings import SettingsCreate, SettingsResponse
from app.services import settings as settings_service

router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
)

SETTINGS_NOT_FOUND = "Settings not found"


@router.get("/")
async def get_settings(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> SettingsResponse | None:
    require_super_admin(current_user)

    settings = await settings_service.get_settings(db)

    if settings is None:
        return None

    return SettingsResponse.model_validate(settings)


@router.post("/")
async def create_settings(
    payload: SettingsCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> SettingsResponse:
    require_super_admin(current_user)

    settings = await settings_service.create_settings(payload, db)

    return SettingsResponse.model_validate(settings)


@router.put(
    "/",
    responses={
        404: {
            "description": SETTINGS_NOT_FOUND,
        },
    },
)
async def update_settings(
    payload: SettingsCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> SettingsResponse:
    require_super_admin(current_user)

    settings = await settings_service.get_settings(db)

    if settings is None:
        raise HTTPException(
            status_code=404,
            detail=SETTINGS_NOT_FOUND,
        )

    updated_settings = await settings_service.update_settings(
        settings,
        payload,
        db,
    )

    return SettingsResponse.model_validate(updated_settings)
