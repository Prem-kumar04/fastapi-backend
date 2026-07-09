from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.rbac import require_admin_or_super_admin
from app.models.module import Module
from app.services import module as module_service

router = APIRouter(
    prefix="/api/modules",
    tags=["modules"],
)


@router.get("/", response_model=None)
async def get_modules(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
    dict[str, Any],
    Depends(get_current_user),
],
) -> list[Module]:
    require_admin_or_super_admin(current_user)

    return await module_service.get_modules(db)
