from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Settings(Base):

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    application_name: Mapped[str]

    company_name: Mapped[str]

    default_language: Mapped[str]

    session_timeout: Mapped[int]

    allow_registration: Mapped[bool]

    enable_notifications: Mapped[bool]

    enable_export_reports: Mapped[bool]

    jwt_enabled: Mapped[bool]

    password_min_length: Mapped[int]

    token_expiry_minutes: Mapped[int]
