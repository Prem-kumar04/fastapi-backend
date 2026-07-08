from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report
from app.schema.report import ReportCreate


async def create_report(
    payload: ReportCreate,
    db: AsyncSession,
) -> Report:
    report = Report(
        title=payload.title,
        description=payload.description,
        created_by=payload.created_by,
    )

    db.add(report)
    await db.commit()
    await db.refresh(report)

    return report


async def get_reports(
    db: AsyncSession,
) -> list[Report]:
    result = await db.execute(
        select(Report)
    )

    return list(result.scalars().all())


async def search_reports(
    keyword: str,
    db: AsyncSession,
) -> list[Report]:
    result = await db.execute(
        select(Report).where(
            Report.title.ilike(f"%{keyword}%")
        )
    )

    return list(result.scalars().all())


async def update_report(
    report_id: int,
    payload: ReportCreate,
    db: AsyncSession,
) -> Report | None:
    result = await db.execute(
        select(Report).where(
            Report.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if report is None:
        return None

    report.title = payload.title
    report.description = payload.description
    report.created_by = payload.created_by

    await db.commit()
    await db.refresh(report)

    return report


async def delete_report(
    report_id: int,
    db: AsyncSession,
) -> dict[str, str] | None:
    result = await db.execute(
        select(Report).where(
            Report.id == report_id
        )
    )

    report = result.scalar_one_or_none()

    if report is None:
        return None

    await db.delete(report)
    await db.commit()

    return {
        "message": "Report deleted successfully",
    }
