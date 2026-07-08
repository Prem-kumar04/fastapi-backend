from datetime import UTC, datetime, timedelta
from typing import Any, Final, cast

from jose import JWTError, jwt

from app.core.settings import Settings

settings = Settings()

SECRET_KEY: Final[str] = settings.secret_key
ALGORITHM: Final[str] = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = 15
REFRESH_TOKEN_EXPIRE_DAYS: Final[int] = 7

ACCESS_TOKEN_TYPE: Final[str] = "access"
REFRESH_TOKEN_TYPE: Final[str] = "refresh"


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "token_type": ACCESS_TOKEN_TYPE,
        }
    )

    return cast(
        "str",
        jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM,
        ),
    )


def create_refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode.update(
        {
            "exp": expire,
            "token_type": REFRESH_TOKEN_TYPE,
        }
    )

    return cast(
        "str",
        jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM,
        ),
    )


def verify_token(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return cast("dict[str, Any]", payload)

    except JWTError as error:
        print("JWT ERROR =", error)
        return None
