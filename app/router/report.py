from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user
from app.core.database import get_db
from app.schema.report import ReportCreate, ReportResponse
from app.services import report as report_service

REPORT_NOT_FOUND = "Report not found"

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
)


@router.get("/")
async def get_reports(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> list[ReportResponse]:
    reports = await report_service.get_reports(db)
    return [ReportResponse.model_validate(report) for report in reports]


@router.post("/")
async def create_report(
    payload: ReportCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> ReportResponse:
    report = await report_service.create_report(payload, db)
    return ReportResponse.model_validate(report)


@router.get("/search")
async def search_reports(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
    keyword: Annotated[
        str,
        Query(
            ...,
            description="Keyword to search reports",
        ),
    ],
) -> list[ReportResponse]:
    reports = await report_service.search_reports(keyword, db)
    return [ReportResponse.model_validate(report) for report in reports]


@router.get("/export")
async def export_reports(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> JSONResponse:
    reports = await report_service.get_reports(db)

    data = [
        {
            "id": report.id,
            "title": report.title,
            "description": report.description,
        }
        for report in reports
    ]

    return JSONResponse(content={"reports": data})


@router.put(
    "/{report_id}",
    responses={
        404: {
            "description": REPORT_NOT_FOUND,
        },
    },
)
async def update_report(
    report_id: int,
    payload: ReportCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> ReportResponse:
    report = await report_service.update_report(report_id, payload, db)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=REPORT_NOT_FOUND,
        )

    return ReportResponse.model_validate(report)


@router.delete(
    "/{report_id}",
    responses={
        404: {
            "description": REPORT_NOT_FOUND,
        },
    },
)
async def delete_report(
    report_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[
        dict[str, Any],
        Depends(get_current_user),
    ],
) -> dict[str, str]:
    result = await report_service.delete_report(report_id, db)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=REPORT_NOT_FOUND,
        )

    return result
