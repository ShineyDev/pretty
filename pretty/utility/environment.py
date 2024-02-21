from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, overload

    _T = TypeVar("_T")

import logging
import os

from pretty.utility import MISSING


_environment_prefix = "PYTHONPRETTY"
environment_logger = f"{_environment_prefix}LOGGER"
environment_logging = f"{_environment_prefix}LOGGING"
environment_root = _environment_prefix
environment_theme = f"{_environment_prefix}THEME"
environment_traceback = f"{_environment_prefix}TRACEBACK"


if TYPE_CHECKING:

    @overload
    def get_environment(
        name: str,
        /,
    ) -> str | None:
        ...

    @overload
    def get_environment(
        name: str,
        /,
        *,
        default: _T,
    ) -> str | _T:
        ...


def get_environment(
    name: str,
    /,
    *,
    default: _T = None,
) -> str | _T:
    return os.environ.get(name, default)


_bool_values_map = {
    False: ["0", "false", "off", "disable", "no", "n"],
    True: ["1", "true", "on", "enable", "yes", "y"],
}
_value_bool_map = {v: k for k in _bool_values_map.keys() for v in _bool_values_map[k]}


if TYPE_CHECKING:

    @overload
    def get_environment_boolean(
        name: str,
        /,
    ) -> bool | None:
        ...

    @overload
    def get_environment_boolean(
        name: str,
        /,
        *,
        default: _T,
    ) -> bool | _T:
        ...


def get_environment_boolean(
    name: str,
    /,
    *,
    default: _T = None,
) -> bool | _T:
    value: str = get_environment(name, default=MISSING)

    if value is MISSING:
        return default

    try:
        return _value_bool_map[value]
    except KeyError:
        return default


if TYPE_CHECKING:

    @overload
    def get_environment_logging(
        name: str,
        /,
    ) -> bool | int | None:
        ...

    @overload
    def get_environment_logging(
        name: str,
        /,
        *,
        default: _T,
    ) -> bool | int | _T:
        ...


def get_environment_logging(
    name: str,
    /,
    *,
    default: _T = None,
) -> bool | int | _T:
    value: str = get_environment(name, default=MISSING)

    if value is MISSING:
        return default

    try:
        boolean = _value_bool_map[value]
    except KeyError:
        pass
    else:
        if boolean is not False:
            return default

    try:
        return logging._nameToLevel[value]
    except KeyError:
        return default


__all__ = [
    "environment_logger",
    "environment_logging",
    "environment_root",
    "environment_theme",
    "environment_traceback",
    "get_environment",
    "get_environment_boolean",
    "get_environment_logging",
]
