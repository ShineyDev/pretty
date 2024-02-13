"""
pretty: A Python library with practical APIs for prettier output.

TODO(introduction)
"""

from __future__ import annotations
from typing import NamedTuple

import json
import logging
import os

import pretty
from pretty import traceback as traceback
from pretty import utility as utility


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


logger = utility.get_logger("pretty")


def _main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    enable_all = pretty.utility.get_environment_boolean("PYTHONPRETTY", default=None)

    if enable_all is False:
        return

    logger.setLevel(pretty.utility.get_environment_logging("PYTHONPRETTYLOGGING", default=logging.INFO))

    theme = pretty.utility.pretty_theme.copy()

    env_theme = os.environ.get("PYTHONPRETTYTHEME")
    if env_theme is not None:
        try:
            user_theme = json.loads(env_theme)
        except json.JSONDecodeError as e:
            logger.error("failed to load PYTHONPRETTYTHEME, falling back to default", e)
        else:
            if isinstance(user_theme, dict):
                theme.update(user_theme)
            else:
                logger.warning("PYTHONPRETTYTHEME not a mapping, falling back to default")

    if pretty.utility.get_environment_boolean("PYTHONPRETTYTRACEBACK", default=enable_all):
        try:
            pretty.traceback.hook(theme=theme)
        except Exception as e:
            logger.error("failed to hook pretty.traceback", e)
        else:
            logger.info("hooked pretty.traceback")


def _main_catchall() -> None:
    try:
        _main()
    except Exception as e:
        logger.error("failed to initialize pretty", e)


__all__ = [
    "traceback",
    "utility",
]
