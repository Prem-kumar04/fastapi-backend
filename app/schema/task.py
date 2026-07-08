from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_employee_id: int | None = None


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    assigned_employee_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    assigned_employee_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
