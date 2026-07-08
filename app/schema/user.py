
from pydantic import BaseModel


class PermissionSchema(BaseModel):
    view: bool = False
    create: bool = False
    edit: bool = False
    delete: bool = False
    export: bool = False  # ✅ this was missing


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role_name: str
    permissions: dict[str, PermissionSchema] = {}


class UserUpdate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role_name: str
    permissions: dict[str, PermissionSchema] | None = None


class ProfileUpdate(BaseModel):
    first_name: str
    last_name: str
    password: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role_name: str

    class Config:
        from_attributes = True
