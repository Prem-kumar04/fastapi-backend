from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.module import Module


async def get_modules(
    db: AsyncSession,
) -> list[Module]:
    result = await db.execute(
        select(Module)
    )

    return list(result.scalars().all())
