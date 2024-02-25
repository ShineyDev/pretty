from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

import sys

from .typing import MISSING


if sys.platform == "win32":
    from .windows import get_console_mode, OutputConsoleMode


def supports_color(
    stream: TextIO = MISSING,
    /,
) -> bool:
    """
    TODO
    """

    if sys.platform == "win32":
        if isinstance(console_mode := get_console_mode(stream), OutputConsoleMode):
            return bool(console_mode & OutputConsoleMode.ENABLE_VIRTUAL_TERMINAL_PROCESSING)

    if stream is MISSING:
        stream = sys.stdout

    return stream.isatty()


__all__ = [
    "supports_color",
]
