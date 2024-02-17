from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Generator
    from typing import Any, overload
    from typing_extensions import TypeAlias, ParamSpec, Self

    _P = ParamSpec("_P")
    _T = TypeVar("_T")
    _U = TypeVar("_U")

    _Generator: TypeAlias = Generator[_T, None, Any]
    _GeneratorFunc: TypeAlias = Callable[_P, Generator[_T, None, Any]]

import collections
import typing

from .typing import MISSING
from .version import SUPPORTS_GENERICBUILTINS


def _make_key(
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> int:
    return hash((args, frozenset(kwargs.items())))


if TYPE_CHECKING:

    @overload
    def cache_generator(
        wrapped: _GeneratorFunc[_P, _T],
        /,
    ) -> _GeneratorFunc[_P, _T]: ...

    @overload
    def cache_generator(
        *,
        max_size: int | None = ...,
    ) -> Callable[[_GeneratorFunc[_P, _T]], _GeneratorFunc[_P, _T]]: ...

    @overload
    def cache_generator(
        *,
        max_size: int | None = ...,
        wrapper: Callable[[_Generator[_T]], _U],
    ) -> Callable[[_GeneratorFunc[_P, _T]], Callable[_P, _U]]: ...


def cache_generator(
    wrapped: _GeneratorFunc[_P, _T] = MISSING,
    /,
    *,
    max_size: int | None = MISSING,
    wrapper: Callable[[_Generator[_T]], _U] = MISSING,
) -> _GeneratorFunc[_P, _T] | Callable[[_GeneratorFunc[_P, _T]], _GeneratorFunc[_P, _T]] | Callable[[_GeneratorFunc[_P, _T]], Callable[_P, _U]]:
    max_size = max_size if max_size is not MISSING else 1024

    if isinstance(max_size, int):
        if max_size < -1 or max_size == 0:
            raise ValueError("max_size must be None, -1, or a positive integer")

    if wrapper is not MISSING:

        def decorator_wrapper(
            wrapped: _GeneratorFunc[_P, _T],
            /,
        ) -> Callable[_P, _U]:
            cache: dict[int, _U] | None

            if max_size == -1 or max_size is None:
                cache = dict()
            else:
                cache = LRUCache(max_size=max_size)

            def inner(
                *args: _P.args,
                **kwargs: _P.kwargs,
            ) -> _U:
                key = _make_key(args, kwargs)

                if key not in cache:
                    cache[key] = wrapper(wrapped(*args, **kwargs))

                return cache[key]

            inner.__utility_cache__ = cache

            return inner

        return decorator_wrapper

    else:

        def decorator(
            wrapped: _GeneratorFunc[_P, _T],
            /,
        ) -> _GeneratorFunc[_P, _T]:
            cache: dict[int, tuple[Generator[_T, None, Any], list[_T], bool]]

            if max_size == -1 or max_size is None:
                cache = dict()
            else:
                cache = LRUCache(max_size=max_size)

            def inner(
                *args: _P.args,
                **kwargs: _P.kwargs,
            ) -> Generator[_T, None, Any]:
                key = _make_key(args, kwargs)

                if key not in cache:
                    generator = wrapped(*args, **kwargs)
                    cache[key] = (generator, list(), False)

                generator, items, done = cache[key]

                i = 0  # NOTE: this garbage is all required to support multiple entries before exit
                while i < len(items):
                    yield items[i]
                    i += 1

                if not done:
                    i = 0
                    for item in generator:
                        items.append(item)
                        yield item
                        i += 1

                        if cache[key][2]:
                            yield from items[i:]
                            return

                    cache[key] = (MISSING, items, True)

            inner.__utility_cache__ = cache

            return inner

        if wrapped is MISSING:
            return decorator

        return decorator(wrapped)


_K = TypeVar("_K")
_V = TypeVar("_V")


class LRUCache(collections.OrderedDict[_K, _V] if SUPPORTS_GENERICBUILTINS else typing.OrderedDict[_K, _V]):  # type: ignore
    """
    TODO
    """

    def __init__(
        self: Self,
        /,
        *,
        max_size: int,
    ) -> None:
        super().__init__()

        self.max_size = max_size

    def __getitem__(self, key: _K) -> _V:
        value = super().__getitem__(key)
        self.move_to_end(key)

        return value

    def __setitem__(self, key: _K, value: _V) -> None:
        if key in self:
            self.move_to_end(key)

        super().__setitem__(key, value)

        if len(self) > self.max_size:
            self.popitem(last=False)


__all__ = [
    "cache_generator",
    "LRUCache",
]
