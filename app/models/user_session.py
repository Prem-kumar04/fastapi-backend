from datetime import UTC, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UserSession(Base):
    __tablename__ = "user_session"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    session_token: Mapped[str]

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC)
    )

    expires_at: Mapped[datetime]
