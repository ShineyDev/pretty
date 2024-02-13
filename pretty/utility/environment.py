from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeVar, overload

    _T = TypeVar("_T")

import os


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


__all__ = [
    "get_environment",
]
