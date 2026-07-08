from pydantic import BaseModel


class PermissionItem(BaseModel):

    module_id: int

    can_view: bool

    can_create: bool

    can_edit: bool

    can_delete: bool


class RolePermissionCreate(BaseModel):

    role_id: int

    permissions: list[PermissionItem]
