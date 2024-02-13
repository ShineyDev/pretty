from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, overload

    _T = TypeVar("_T")

import logging
import os

from pretty.utility.transform import try_integer
from pretty.utility.typing import MISSING


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


if TYPE_CHECKING:

    @overload
    def get_environment_logging(
        name: str,
        /,
    ) -> int | None:
        ...

    @overload
    def get_environment_logging(
        name: str,
        /,
        *,
        default: _T,
    ) -> int | _T:
        ...


def get_environment_logging(
    name: str,
    /,
    *,
    default: _T = None,
) -> int | _T:
    value: str = get_environment(name, default=MISSING)

    if value is MISSING:
        return default

    integer: int = try_integer(value, default=MISSING)

    if integer is not MISSING:
        return integer

    try:
        return logging._nameToLevel[value]
    except KeyError:
        return default


__all__ = [
    "get_environment",
    "get_environment_logging",
]
