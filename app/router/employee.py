from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schema.employee import EmployeeResponse
from app.services import employee as employee_service

router = APIRouter(
    prefix="/api/employees",
    tags=["employees"],
)


@router.get("/", response_model=list[EmployeeResponse])
async def get_employees(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[EmployeeResponse]:
    employees = await employee_service.get_employees(db)
    return [EmployeeResponse.model_validate(employee) for employee in employees]
