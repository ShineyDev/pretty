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
from pretty.utility import MISSING


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


logger = logging.getLogger("pretty")


def _main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    enable_all = pretty.utility.get_environment_boolean("PYTHONPRETTY", default=MISSING)

    if enable_all is False:
        return

    # NOTE: when pretty is initialized via pretty.pth, logging needs to
    #       be enabled with some defaults by default. notably,
    if (level := pretty.utility.get_environment_logging("PYTHONPRETTYLOGGING", default=logging.WARNING)) is not False:
        #   we want to hide from user-defined handlers;
        logger.propagate = False
        #   we want to use a very simple format;
        formatter = logging.Formatter(logging.BASIC_FORMAT)  # TODO: special minimal format for exceptions here
        #   we want to write to the *current* stderr stream; and
        handler = utility.CurrentStandardErrorStreamHandler()
        handler.setFormatter(formatter)
        #   we want to see WARNING, ERROR, and CRITICAL messages.
        logger.setLevel(level)
    #       like much else in pretty, this behavior is customizable;
    #       users are able to disable the logger via
    #       PYTHONPRETTYLOGGING=0 or update the level of the logger via
    #       PYTHONPRETTYLOGGING=DEBUG.

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
