from pydantic import BaseModel


class SettingsCreate(BaseModel):

    application_name: str

    company_name: str

    default_language: str

    session_timeout: int

    allow_registration: bool

    enable_notifications: bool

    enable_export_reports: bool

    jwt_enabled: bool

    password_min_length: int

    token_expiry_minutes: int


class SettingsResponse(SettingsCreate):

    id: int

    class Config:

        from_attributes = True
