from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.core.rbac import require_admin_or_super_admin
from app.services import dashboard

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
)


@router.get("/stats")
async def get_dashboard_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
    dict[str, Any],
    Depends(get_current_user),
],
) -> dict[str, Any]:
    require_admin_or_super_admin(current_user)

    return await dashboard.get_dashboard_stats(db)
