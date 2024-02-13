from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, TypeVar, overload

    _T = TypeVar("_T")


if TYPE_CHECKING:

    @overload
    def try_integer(
        value: Any,
        /,
    ) -> int | None:
        ...

    @overload
    def try_integer(
        value: Any,
        /,
        *,
        default: _T,
    ) -> int | _T:
        ...


def try_integer(
    value: Any,
    /,
    *,
    default: _T = None,
) -> int | _T:
    try:
        return int(value)
    except ValueError:
        return default


__all__ = [
    "try_integer",
]
