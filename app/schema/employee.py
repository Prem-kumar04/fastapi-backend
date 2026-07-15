from pydantic import BaseModel, ConfigDict


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: float

    model_config = ConfigDict(from_attributes=True)
