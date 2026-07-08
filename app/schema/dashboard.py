from pydantic import BaseModel


class DashboardStats(BaseModel):

    total_users: int

    active_users: int

    total_roles: int

    total_reports: int

    total_tasks: int
