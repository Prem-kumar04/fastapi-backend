from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    department: Mapped[str]
    salary: Mapped[float]
