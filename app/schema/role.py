
from pydantic import BaseModel


class PermissionItem(BaseModel):
    module_id: int
    can_view: bool = False
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False


class RoleCreate(BaseModel):
    name: str
    description: str
    permissions: list[PermissionItem] | None = []


class RoleUpdate(BaseModel):
    name: str
    description: str
    permissions: list[PermissionItem] | None = []


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
