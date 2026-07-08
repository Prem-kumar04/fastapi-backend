import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.core.database import DBSessionManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[Any]:

    yield

    # Skip closing DB during pytest
    if os.getenv("PYTEST_CURRENT_TEST"):
        return

    if DBSessionManager.engine is not None:
        await DBSessionManager.close()
