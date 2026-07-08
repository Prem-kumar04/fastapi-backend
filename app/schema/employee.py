from pydantic import BaseModel


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    salary: float
