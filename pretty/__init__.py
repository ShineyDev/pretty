"""
pretty: A Python library with practical APIs for prettier output.

TODO(introduction)
"""

from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

import json
import logging
import os

import pretty
from pretty import traceback as traceback
from pretty import utility as utility
from pretty.utility import MISSING


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


logger = logging.getLogger(__name__)


def hook(
    *,
    theme: dict[str, Any] = MISSING,
) -> None:
    """
    Hooks pretty into the current Python session.

    This function respects the value of all
    :term:`PYTHONPRETTY* <PYTHONPRETTYTRACEBACK>` environment variables
    except for :term:`PYTHONPRETTY` and :term:`PYTHONPRETTYTHEME`,
    effectively allowing users to delay the initialization of pretty.

    .. tip::

        You can set the :term:`PYTHONPRETTY` environment variable to a
        :term:`truthy value <boolean value>` to hook pretty into all
        Python sessions.
    """

    theme = theme if theme is not MISSING else utility.pretty_theme.copy()

    _hook(True, theme=theme)


def _hook(
    enable_all: bool,
    *,
    theme: dict[str, Any],
) -> None:
    if pretty.utility.get_environment_boolean(utility.environment_traceback, default=enable_all):
        try:
            pretty.traceback.hook(theme=theme)
        except Exception:
            logger.exception("an unexpected error occurred during initialization of pretty.traceback")
        else:
            logger.info("hooked pretty.traceback")


def _main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    enable_all = pretty.utility.get_environment_boolean(utility.environment_root, default=MISSING)

    if enable_all is False:
        return

    # NOTE: when pretty is initialized via pretty.pth, logging needs to
    #       be enabled with some defaults by default. notably,
    if (level := pretty.utility.get_environment_logging(utility.environment_logger, default=logging.WARNING)) is not False:
        #   we want to hide from user-defined handlers;
        logger.propagate = False
        #   we want to use a very simple format;
        formatter = utility.MinimalExceptionFormatter(logging.BASIC_FORMAT)
        #   we want to write to the *current* stderr stream; and
        handler = utility.CurrentStandardErrorStreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        #   we want to see WARNING, ERROR, and CRITICAL messages.
        logger.setLevel(level)
    #       like much else in pretty, this behavior is customizable;
    #       users are able to disable the logger with a falsey boolean
    #       value or update the level of the logger with a value equal
    #       to a key in the logging._nameToLevel mapping.

    theme = pretty.utility.pretty_theme.copy()

    env_theme = os.environ.get(utility.environment_theme)
    if env_theme is not None:
        try:
            user_theme = json.loads(env_theme)
        except json.JSONDecodeError:
            logger.exception(f"value in {utility.environment_theme} is not valid json, falling back to default")
        else:
            if isinstance(user_theme, dict):
                theme.update(user_theme)
            else:
                logger.error(f"value in {utility.environment_theme} is not a mapping, falling back to default")

    _hook(enable_all, theme=theme)


def _main_catchall() -> None:
    logger.debug("initialization start")

    try:
        _main()
    except Exception:
        logger.exception("an unexpected error occurred during initialization of pretty")

    logger.debug("initialization end")


__all__ = [
    "traceback",
    "utility",
]
