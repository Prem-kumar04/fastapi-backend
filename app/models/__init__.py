from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Register the models for Migration
from . import customer as customer
from . import employee as employee
from . import module as module
from . import order as order
from . import product as product
from . import refresh_token as refresh_token
from . import report as report
from . import role as role
from . import role_permission as role_permission
from . import settings as settings
from . import task as task
from . import user as user
from . import user_permission as user_permission  # ✅ fixed — same style as all others
from . import user_session as user_session
