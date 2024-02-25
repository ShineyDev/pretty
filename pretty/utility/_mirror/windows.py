from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO

import ctypes
import enum
import subprocess
import sys

from .typing import MISSING


assert sys.platform == "win32"


import ctypes.wintypes
import msvcrt


def get_console_mode(
    stream: TextIO = MISSING,
    /,
) -> InputConsoleMode | OutputConsoleMode:
    """
    TODO
    """

    if stream:
        handle = msvcrt.get_osfhandle(stream.fileno())
    else:
        handle = ctypes.windll.kernel32.GetStdHandle(subprocess.STD_OUTPUT_HANDLE)

    mode = ctypes.wintypes.DWORD()

    if ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode)) == 0:
        raise ctypes.WinError(ctypes.get_last_error())

    if stream is MISSING or stream.writable():
        return OutputConsoleMode(mode.value)
    else:
        return InputConsoleMode(mode.value)


class InputConsoleMode(enum.IntFlag):
    # fmt: off
    ENABLE_PROCESSED_INPUT        = 0b0000000001
    ENABLE_LINE_INPUT             = 0b0000000010
    ENABLE_ECHO_INPUT             = 0b0000000100
    ENABLE_WINDOW_INPUT           = 0b0000001000
    ENABLE_MOUSE_INPUT            = 0b0000010000
    ENABLE_INSERT_MODE            = 0b0000100000
    ENABLE_QUICK_EDIT_MODE        = 0b0001000000
    ENABLE_EXTENDED_FLAGS         = 0b0010000000
    ENABLE_AUTO_POSITION          = 0b0100000000
    ENABLE_VIRTUAL_TERMINAL_INPUT = 0b1000000000
    # fmt: on


class OutputConsoleMode(enum.IntFlag):
    # fmt: off
    ENABLE_PROCESSED_OUTPUT            = 0b00001
    ENABLE_WRAP_AT_EOL_OUTPUT          = 0b00010
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0b00100
    DISABLE_NEWLINE_AUTO_RETURN        = 0b01000
    ENABLE_LVB_GRID_WORLDWIDE          = 0b10000
    # fmt: on


__all__ = [
    "get_console_mode",
    "InputConsoleMode",
    "OutputConsoleMode",
]
