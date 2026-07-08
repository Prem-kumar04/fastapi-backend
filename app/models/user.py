
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    slug: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    first_name: Mapped[str]

    last_name: Mapped[str]

    password: Mapped[str]

    role_id: Mapped[int | None] = mapped_column(
        ForeignKey("role.id"),
        nullable=True
    )
