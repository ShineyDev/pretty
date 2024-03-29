from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Sequence, TypeVar

import os
import sys


if TYPE_CHECKING:
    _T = TypeVar("_T")


# NOTE: SGR color values are HSV(x°, 30%, 100%) where;
#
#       x     SGR           name
#       ---   -----------   ---------
#       0     255;179;179   red
#       30    255;217;179   orange
#       60    255;255;179   yellow
#       90    217;255;179   lime
#       120   179;255;179   green
#       150   179;255;217   turquoise
#       180   179;255;255   cyan
#       210   179;217;255   blue
#       240   179;179;255   indigo
#       270   217;179;255   purple
#       300   255;179;255   magenta
#       330   255;179;217   pink
#
#       SGR grayscale values are HSV(0°, 0%, y%) where;
#
#       y     SGR           name
#       --    -----------   -----
#       10    26;26;26      black
#       25    64;64;64      dark gray
#       50    128;128;128   middle gray
#       75    191;191;191   light gray
#       90    230;230;230   white
#
pretty_theme: dict[str, Any] = {
    # colorizing abstract syntax trees
    "ast_comment_sgr": ("38;2;179;255;179", "39"),
    "ast_delimiter_sgr": ("38;2;128;128;128", "39"),
    "ast_keyword_sgr": ("38;2;179;179;255", "39"),
    "ast_name_sgr": ("38;2;191;191;191", "39"),
    "ast_operator_sgr": ("38;2;128;128;128", "39"),
    # customizing character display
    "char_cap": "\u2514",
    "char_pathnamesep": os.sep,
    "char_pipe": "\u2502",
    "char_quote": "'",
    # colorizing literal types
    "literal_bool_sgr": ("38;2;179;179;255", "39"),
    "literal_bytes_sgr": ("38;2;255;217;179", "39"),
    "literal_complex_sgr": ("38;2;179;255;255", "39"),
    "literal_ellipsis_sgr": ("38;2;128;128;128", "39"),
    "literal_float_sgr": ("38;2;179;255;255", "39"),
    "literal_int_sgr": ("38;2;179;255;255", "39"),
    "literal_none_sgr": ("38;2;179;179;255", "39"),
    "literal_str_sgr": ("38;2;255;217;179", "39"),
    # pretty.traceback
    "traceback_exception_sgr": ("38;2;255;179;179", "39"),
    "traceback_filename_sgr": ("38;2;230;230;230", "39"),
    "traceback_introspection_sgr": ("38;2;255;179;255", "39"),
    "traceback_lineno_sgr": ("38;2;255;179;255", "39"),
    "traceback_location_sgr": None,
    "traceback_name_sgr": ("38;2;230;230;230", "39"),
    "traceback_header_sgr": ("38;2;230;230;230", "39"),
    "traceback_message_sgr": ("38;2;128;128;128", "39"),
    "traceback_scope_key_sgr": ("38;2;191;191;191", "39"),
    "traceback_source_sgr": None,
}


def rindex(
    iterable: Sequence[_T],
    value: _T,
    *,
    start: int | None = None,
    end: int | None = None,
) -> int:
    if (isinstance(iterable, bytes) and isinstance(value, bytes)) or (isinstance(iterable, bytes) and isinstance(value, bytes)):
        return iterable.rindex(value, start, end)

    iterable_length = len(iterable)

    for reversed_i, element in enumerate(reversed(iterable), 1):
        i = iterable_length - reversed_i

        if start is not None and i < start:
            break
        if end is not None and i > end:
            break

        if element == value:
            return i

    raise ValueError("value not found in iterable")


def sweeten(
    string: str,
    sgr: str | tuple[str, str] | None,
) -> str:
    if not sgr:
        return string

    ansi_enabled = try_bool(os.environ.get("PYTHONPRETTYANSI"), default=None)
    if (ansi_enabled is None and try_bool(os.environ.get("NO_COLOR"), default=None)) or ansi_enabled is None or not ansi_enabled:
        return string

    if isinstance(sgr, str):
        sgr_start, sgr_end = sgr, "0"
    else:
        sgr_start, sgr_end = sgr

    return f"\x1B[{sgr_start}m{string}\x1B[{sgr_end}m"


def try_attr(
    obj: Any,
    name: str,
    *,
    default: Any,
) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return default


_bool_map = {
    False: ["0", "false", "off", "disable", "no", "n"],
    True: ["1", "true", "on", "enable", "yes", "y"],
}
_bool_map = {v: k for k in _bool_map.keys() for v in _bool_map[k]}


def try_name(
    obj: Any,
    *,
    default: _T,
) -> str | _T:
    name = try_attr(obj, "__qualname__", default=None) or try_attr(obj, "__name__", default=None)
    if not name:
        return default

    module = try_attr(obj, "__module__", default=None)

    if module and isinstance(module, str) and module not in ("__main__", "builtins"):
        module_names = module.split(".")

        i = len(module_names)
        while i:
            module_test = ".".join(module_names[:i])

            try:
                module_type = sys.modules[module_test]
            except KeyError:
                break

            obj_test = module_type
            for part in name.split("."):
                obj_test = try_attr(obj_test, part, default=None)
                if obj_test is None:
                    break

            if obj_test is not obj:
                break

            module = module_test

            i -= 1

        name = f"{module}.{name}"

    return name


def try_repr(
    obj: Any,
    *,
    default: _T,
) -> str | _T:
    try:
        return repr(obj)
    except Exception:
        return default


def try_str(
    obj: Any,
    *,
    default: _T,
) -> str | _T:
    try:
        return str(obj)
    except Exception:
        return default


__all__ = [
    "rindex",
    "sweeten",
    "try_attr",
    "try_name",
    "try_repr",
    "try_str",
]
