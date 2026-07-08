from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.settings import Settings
from app.schema.settings import SettingsCreate


async def get_settings(
    db: AsyncSession,
) -> Settings | None:
    result = await db.execute(
        select(Settings)
    )

    return result.scalar_one_or_none()


async def create_settings(
    payload: SettingsCreate,
    db: AsyncSession,
) -> Settings:
    settings = Settings(
        application_name=payload.application_name,
        company_name=payload.company_name,
        default_language=payload.default_language,
        session_timeout=payload.session_timeout,
        allow_registration=payload.allow_registration,
        enable_notifications=payload.enable_notifications,
        enable_export_reports=payload.enable_export_reports,
        jwt_enabled=payload.jwt_enabled,
        password_min_length=payload.password_min_length,
        token_expiry_minutes=payload.token_expiry_minutes,
    )

    db.add(settings)

    await db.commit()

    await db.refresh(settings)

    return settings


async def update_settings(
    settings: Settings,
    payload: SettingsCreate,
    db: AsyncSession,
) -> Settings:
    settings.application_name = payload.application_name
    settings.company_name = payload.company_name
    settings.default_language = payload.default_language
    settings.session_timeout = payload.session_timeout
    settings.allow_registration = payload.allow_registration
    settings.enable_notifications = payload.enable_notifications
    settings.enable_export_reports = payload.enable_export_reports
    settings.jwt_enabled = payload.jwt_enabled
    settings.password_min_length = payload.password_min_length
    settings.token_expiry_minutes = payload.token_expiry_minutes

    await db.commit()

    await db.refresh(settings)

    return settings
