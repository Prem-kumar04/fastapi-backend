from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Module(Base):

    __tablename__ = "module"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )
