from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report
from app.models.role import Role
from app.models.task import Task
from app.models.user import User


async def get_dashboard_stats(
    db: AsyncSession,
) -> dict[str, Any]:
    users_result = await db.execute(
        select(func.count(User.id))
    )

    roles_result = await db.execute(
        select(func.count(Role.id))
    )

    reports_result = await db.execute(
        select(func.count(Report.id))
    )

    tasks_result = await db.execute(
        select(func.count(Task.id))
    )

    total_users = users_result.scalar() or 0
    total_roles = roles_result.scalar() or 0
    total_reports = reports_result.scalar() or 0
    total_tasks = tasks_result.scalar() or 0

    return {
        "total_users": total_users,
        "active_users": total_users,
        "total_roles": total_roles,
        "total_reports": total_reports,
        "total_tasks": total_tasks,
    }
