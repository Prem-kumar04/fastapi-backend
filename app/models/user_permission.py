from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from . import Base


class UserPermission(Base):

    __tablename__ = "user_permission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False
    )

    module: Mapped[str] 

    view: Mapped[bool] = mapped_column(default=False)
    create: Mapped[bool] = mapped_column(default=False)
    edit: Mapped[bool] = mapped_column(default=False)
    delete: Mapped[bool] = mapped_column(default=False)
    export: Mapped[bool] = mapped_column(default=False)  # ✅ new column