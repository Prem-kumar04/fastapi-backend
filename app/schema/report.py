from pydantic import BaseModel


class ReportCreate(BaseModel):

    title: str

    description: str

    created_by: str


class ReportResponse(BaseModel):

    id: int

    title: str

    description: str

    created_by: str

    class Config:

        from_attributes = True
