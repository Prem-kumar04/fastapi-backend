from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Role(Base):

    __tablename__ = "role"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    description: Mapped[str] = mapped_column()
