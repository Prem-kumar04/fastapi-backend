from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.jwt import create_access_token, create_refresh_token, verify_token
from app.models.role import Role
from app.schema.auth import LoginRequest, SignupRequest
from app.schema.user import UserCreate
from app.services import user as user_service

ROLE_NOT_FOUND = "Role not found"
INVALID_CREDENTIALS = "Invalid credentials"
INVALID_REFRESH_TOKEN = "Invalid refresh token"  # nosec B105
INVALID_TOKEN_TYPE = "Invalid token type"  # nosec B105

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post(
    "/signup",
    responses={
        404: {
            "description": ROLE_NOT_FOUND,
        },
    },
)
async def signup(
    payload: SignupRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> object:
    role_result = await db.execute(
        select(Role).where(Role.id == payload.role_id)
    )
    role = role_result.scalar_one_or_none()

    if role is None:
        raise HTTPException(
            status_code=404,
            detail=ROLE_NOT_FOUND,
        )

    user = UserCreate(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        password=payload.password,
        role_name=role.name,
        permissions={},
    )

    return await user_service.create_user(user, db)


@router.post(
    "/login",
    responses={
        401: {
            "description": INVALID_CREDENTIALS,
        },
    },
)
async def login(
    payload: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> object:
    user = await user_service.get_user_by_email(
        payload.email,
        db,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail=INVALID_CREDENTIALS,
        )

    if user.password != payload.password:
        raise HTTPException(
            status_code=401,
            detail=INVALID_CREDENTIALS,
        )

    role_result = await db.execute(
        select(Role).where(Role.id == user.role_id)
    )
    role = role_result.scalar_one_or_none()

    role_name = ""
    if role is not None:
        role_name = role.name.lower().replace(" ", "_")

    permissions = await user_service.get_user_permissions(
        user.id,
        db,
    )

    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "role": role_name,
    }

    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.id,
        "role": role_name,
        "permissions": permissions,
    }


@router.post(
    "/refresh",
    responses={
        401: {
            "description": "Unauthorized",
        },
    },
)
async def refresh_token(
    payload: dict[str, str],
) -> dict[str, str]:
    refresh_token_value = payload.get("refresh_token", "")

    token_data = verify_token(refresh_token_value)

    if token_data is None:
        raise HTTPException(
            status_code=401,
            detail=INVALID_REFRESH_TOKEN,
        )

    if token_data.get("token_type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail=INVALID_TOKEN_TYPE,
        )

    access_token = create_access_token(
        {
            "user_id": token_data["user_id"],
            "email": token_data["email"],
            "role": token_data["role"],
        }
    )

    return {
        "access_token": access_token,
    }
