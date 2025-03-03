import typing

from fastapi.logger import logger as fastapi_logger
from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "task_manager"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: typing.Dict[str, typing.Dict[str, str]] = {
        "default": {
            "format": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: typing.Dict[str, typing.Dict[str, typing.Any]] = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }
    loggers: typing.Dict[str, typing.Dict[str, typing.Any]] = {
        LOGGER_NAME: {
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    }

import logging.config
logging.config.dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LogConfig().LOGGER_NAME)

fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)