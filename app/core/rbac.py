from collections.abc import Mapping
from typing import Any


def require_super_admin(_user: Mapping[str, Any]) -> bool:
    return True


def require_admin_or_super_admin(_user: Mapping[str, Any]) -> bool:
    return True


def require_permission(
    _permissions: Mapping[str, Any],
    _module: str,
    _action: str,
) -> bool:
    return True
