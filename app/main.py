from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app import logger
from app.core.config import setup_logger
from app.core.manager import lifespan
from app.core.redis import RedisHelper
from app.core.settings import Settings
from app.router import module, role_permission
from app.router.base import router as base_router
from app.router.dashboard import router as dashboard_router
from app.router.employee import router as employee_router
from app.router.report import router as report_router
from app.router.role import router as role_router
from app.router.settings import router as settings_router
from app.router.task import router as task_router
from app.router.user import router as user_router
from app.router.users import router as users_router

_settings = Settings()

app = FastAPI(
    lifespan=lifespan,
    debug=_settings.debug,
    docs_url="/api/docs"
)

# ✅ CORS must be added FIRST before any routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

setup_logger(_settings.debug)

# Routers added AFTER middleware
app.include_router(role_permission.router)
app.include_router(module.router)

# Authentication
app.include_router(user_router)

# Base
app.include_router(base_router)

# Dashboard
app.include_router(dashboard_router)

# Users
app.include_router(users_router)

# Roles
app.include_router(role_router)

# Reports
app.include_router(report_router)

# Employees
app.include_router(employee_router)

# Tasks
app.include_router(task_router)

# Settings
app.include_router(settings_router)


client = TestClient(app)


def add_cache_layer(app: FastAPI) -> None:
    try:
        app.state.cache = RedisHelper()
    except Exception as e:
        logger.error(e)
