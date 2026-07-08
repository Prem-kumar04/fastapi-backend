from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Report(Base):

    __tablename__ = "report"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    title: Mapped[str]

    description: Mapped[str]

    created_by: Mapped[str]
