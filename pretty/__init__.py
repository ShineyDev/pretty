"""
pretty: A Python library with practical APIs for prettier output.

TODO(introduction)
"""

from __future__ import annotations
from typing import NamedTuple

import json
import os
import sys

import pretty
from pretty import traceback as traceback
from pretty import utils as utils


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


def _fail(e: Exception, m: str) -> None:
    if hasattr(sys, "last_value") and sys.last_value is not None:
        print(f"ERROR:pretty:{m}.")
    else:
        sys.last_type, sys.last_value, sys.last_traceback = type(e), e, e.__traceback__
        print(f"ERROR:pretty:{m}. see traceback.print_last().")


def _main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    enable_all = pretty.utils.try_bool(os.environ.get("PYTHONPRETTY"), default=None)

    if enable_all is False:
        return

    theme = pretty.utils.pretty_theme.copy()

    env_theme = os.environ.get("PYTHONPRETTYTHEME")
    if env_theme is not None:
        try:
            user_theme = json.loads(env_theme)
        except json.JSONDecodeError as e:
            _fail(e, "failed to load PYTHONPRETTYTHEME, falling back to default")
        else:
            if isinstance(user_theme, dict):
                theme.update(user_theme)

    if pretty.utils.try_bool(os.environ.get("PYTHONPRETTYTRACEBACK"), default=enable_all):
        try:
            pretty.traceback.hook(theme=theme)
        except Exception as e:
            _fail(e, "failed to hook pretty.traceback")


def _main_catchall() -> None:
    try:
        _main()
    except Exception as e:
        _fail(e, "failed to initialize pretty")


__all__ = [
    "traceback",
    "utils",
]
