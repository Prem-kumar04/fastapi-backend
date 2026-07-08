from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    address: Mapped[str]
