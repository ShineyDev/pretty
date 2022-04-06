from __future__ import annotations
from typing import NamedTuple

import json
import os
import sys

from pretty import utils
from pretty import traceback


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "2.0.0a"
version_info: _VersionInfo = _VersionInfo(2, 0, 0, "alpha", 0)


def main() -> None:
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    enable_all = utils.try_bool(os.environ.get("PYTHONPRETTY"), default=None)

    if enable_all is False:
        return

    def _fail(e, m):
        if hasattr(sys, "last_value"):
            print(f"ERROR:pretty:{m}")
        else:
            print(f"ERROR:pretty:{m} see traceback.print_last().")
            sys.last_type, sys.last_value, sys.last_traceback = type(e), e, e.__traceback__

    theme = utils.pretty_theme.copy()

    env_theme = os.environ.get("PYTHONPRETTYTHEME")
    if env_theme is not None:
        try:
            user_theme = json.loads(env_theme)
        except json.JSONDecodeError as e:
            _fail(e, "failed to load PYTHONPRETTYTHEME, falling back to default.")
        else:
            theme.update(user_theme)

    enable_traceback = utils.try_bool(os.environ.get("PYTHONPRETTYTRACEBACK"), default=False)

    if enable_all or enable_traceback:
        try:
            traceback.hook(theme=theme)
        except Exception as e:
            _fail(e, "failed to hook pretty.traceback.")


__all__ = []
