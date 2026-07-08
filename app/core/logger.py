import logging

from loguru import logger as _log

LOG_ROTATION = "1 day"
LOG_COMPRESSION = "zip"
LOG_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level} | "
    "{module}:{function}:{line} | "
    "{message}"
)


def setup_logger(with_debug: bool = False) -> None:
    log_path = "data/logs"

    # App Info Log
    _log.add(
        f"{log_path}/app.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        filter=lambda record: record["extra"].get("context")
        not in {"system", "comm", "trade"},
        level="INFO",
    )

    # App Error logs
    _log.add(
        f"{log_path}/error.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        filter=lambda record: (
            record["extra"].get("context")
            not in {"system", "comm", "trade"}
            and record["level"].name in {"ERROR", "CRITICAL"}
        ),
        level="DEBUG" if with_debug else "ERROR",
    )

    # System logs
    _log.add(
        f"{log_path}/system.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        level="DEBUG" if with_debug else "INFO",
        filter=lambda record: record["extra"].get("context") == "system",
        format=LOG_FORMAT,
    )

    # Communication logs
    _log.add(
        f"{log_path}/comm.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        level="DEBUG" if with_debug else "INFO",
        filter=lambda record: record["extra"].get("context") == "comm",
        format=LOG_FORMAT,
    )

    # Background Job logs
    _log.add(
        f"{log_path}/job.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        level="DEBUG" if with_debug else "INFO",
        filter=lambda record: record["extra"].get("context") == "job",
        format=LOG_FORMAT,
    )

    # External logs
    _log.add(
        f"{log_path}/external.log",
        rotation=LOG_ROTATION,
        compression=LOG_COMPRESSION,
        level="DEBUG" if with_debug else "INFO",
        filter=lambda record: record["extra"].get("context") == "external",
        format=LOG_FORMAT,
    )


# System Logger
slogger = _log.bind(context="system")

# Communication Logger
clogger = _log.bind(context="comm")

# Job Logger
jlogger = _log.bind(context="job")

# External Logger
elogger = _log.bind(context="external")

# Generic Logger
logger = _log


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logger_opt = logger.opt(
            depth=6,
            exception=record.exc_info if record.exc_info else None,
        )
        logger_opt.log(record.levelname, record.getMessage())


logging.basicConfig(
    handlers=[InterceptHandler()],
    level=logging.INFO,
)
