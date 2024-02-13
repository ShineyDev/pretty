from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

import logging


def get_logger(
    name: str,
    /,
) -> Logger:
    manager = logging.Logger.manager

    logging._acquireLock()  # type: ignore  # _acquireLock does exist

    if (l := manager.loggerDict.get(name)) and not isinstance(l, logging.PlaceHolder):
        logging._releaseLock()  # type: ignore  # _releaseLock does exist
        return manager.getLogger(name)

    logging._releaseLock()  # type: ignore  # _releaseLock does exist

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(logging.BASIC_FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


__all__ = [
    "get_logger",
]
