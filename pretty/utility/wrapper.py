from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TypeVar
    from typing_extensions import ParamSpec

    _P = ParamSpec("_P")
    _T = TypeVar("_T")


def wrap_fallback(
    wrapped: Callable[_P, _T],
    /,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    def decorator(
        wrapper: Callable[_P, _T],
        /,
    ) -> Callable[_P, _T]:
        def inner(
            *args: _P.args,
            **kwargs: _P.kwargs,
        ) -> _T:
            try:
                return wrapper(*args, **kwargs)
            except Exception:
                return wrapped(*args, **kwargs)

        inner.__doc__ = wrapped.__doc__
        inner.__name__ = wrapped.__name__
        inner.__qualname__ = wrapped.__qualname__

        inner.__wrapped__ = wrapper
        wrapper.__wrapped__ = wrapped

        return inner

    return decorator


__all__ = [
    "wrap_fallback",
]
