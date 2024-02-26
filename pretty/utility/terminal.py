from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

from pretty.utility import apply_ansi_sgr as _apply_ansi_sgr, wants_ansi_sgr as _wants_ansi_sgr, MISSING
from pretty.utility.environment import get_environment_boolean, environment_color


def apply_ansi_sgr(
    string: str,
    sgr: str | tuple[str, str] | None,
    /,
    *,
    stream: TextIO = MISSING,
) -> str:
    """
    TODO
    """

    if sgr is None:
        return string

    if stream is not MISSING and not wants_ansi_sgr(stream):
        return string

    return _apply_ansi_sgr(string, sgr, stream=stream)


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

    return _wants_ansi_sgr(stream)


__all__ = [
    "apply_ansi_sgr",
    "wants_ansi_sgr",
]
