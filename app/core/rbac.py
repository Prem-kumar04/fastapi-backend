from collections.abc import Mapping
from typing import Any


def require_super_admin(user: Mapping[str, Any]) -> bool:
    return True


def require_admin_or_super_admin(user: Mapping[str, Any]) -> bool:
    return True


def require_permission(
    permissions: Mapping[str, Any],
    module: str,
    action: str,
) -> bool:
    return True
