from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee


async def get_employees(
    db: AsyncSession,
) -> list[Employee]:
    result = await db.execute(
        select(Employee)
    )

    return list(result.scalars().all())
