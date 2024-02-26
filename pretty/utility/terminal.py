from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

import os
import sys

from pretty.utility import supports_ansi, MISSING
from pretty.utility.environment import get_environment_boolean, environment_color


def wants_ansi_sgr(
    stream: TextIO = MISSING,
    /,
) -> bool:
    """
    Determines whether a stream advertises that it both wants and
    supports ANSI SGR escape sequences to be used in its output.

    Specifically, this function does the following, in this order:

    - If the stream advertises that it wants ANSI SGR escape sequences
      continue, otherwise return False.
        - If :term:`PYTHONPRETTYCOLOR` is set to a
          :term:`falsey value <boolean value>` return False.
        - On Python 3.13 and higher, if the environment variable
          |PYTHON_COLORS| is set to ``"0"`` return False.
        - If the environment variable |NO_COLOR| is set with any value
          return False.
        - If the environment variable |FORCE_COLOR| is set with any
          value return True.
        - If the environment variable "TERM" is set to ``"dumb"``
          return False.
    - If the stream advertises that it supports ANSI escape sequences
      return True, otherwise return False.


    Parameters
    ----------
    stream: :class:`~io.TextIO`
        A :class:`text <str>` stream.


    Returns
    -------
    :class:`bool`
        Whether the stream advertises that it both supports and wants
        ANSI SGR escape sequences to be used in its output.
    """

    if get_environment_boolean(environment_color) is False:
        return False

    if sys.version_info >= (3, 13):
        if os.environ.get("PYTHON_COLORS") == "0":
            return False

    if "NO_COLOR" in os.environ.keys():
        return False

    if "FORCE_COLOR" in os.environ.keys():
        return True

    if os.environ.get("TERM") == "dumb":
        return False

    return supports_ansi(stream)


__all__ = [
    "wants_ansi_sgr",
]
