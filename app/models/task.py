from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    title: Mapped[str]

    description: Mapped[str]

    status: Mapped[str] = mapped_column(
        default="Pending"
    )

    assigned_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employee.id"),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
