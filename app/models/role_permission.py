from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class RolePermission(Base):

    __tablename__ = "role_permission"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id")
    )

    module_id: Mapped[int] = mapped_column(
        ForeignKey("module.id")
    )

    can_view: Mapped[bool] = mapped_column(
        default=False
    )

    can_create: Mapped[bool] = mapped_column(
        default=False
    )

    can_edit: Mapped[bool] = mapped_column(
        default=False
    )

    can_delete: Mapped[bool] = mapped_column(
        default=False
    )
