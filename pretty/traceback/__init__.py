from __future__ import annotations
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable, TypeVar
    from typing_extensions import ParamSpec

import sys
import traceback

from pretty.traceback.formatter import *
from pretty.traceback.formatter import __all__ as _formatter__all__


if TYPE_CHECKING:
    _P = ParamSpec("_P")
    _TTF = TypeVar("_TTF", bound=TracebackFormatter)


@overload
def hook(cls: None = ..., *, theme: dict[str, Any] = ...) -> PrettyTracebackFormatter:
    ...


@overload
def hook(cls: Callable[_P, _TTF] = ..., *args: _P.args, **kwargs: _P.kwargs) -> _TTF:
    ...


def hook(cls: Callable[_P, _TTF] | None = None, *args: _P.args, **kwargs: _P.kwargs) -> _TTF | PrettyTracebackFormatter:
    """
    Hooks pretty.traceback into the current Python session.

    .. note::

        You can set the :term:`PYTHONPRETTYTRACEBACK` environment
        variable to a :term:`truthy value <boolean value>` to hook
        pretty.traceback into all Python sessions.

    .. warning::

        This will replace classes and functions in the :mod:`traceback`
        module with attributes and methods from the formatter. All
        callables will fall back to their original implementation on
        exception.

        In order to maintain backward-compatibility with original
        implementations, the following **cannot** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` callables:

        - Any parameter kind, name, order, or type of a callable.
        - The return or yield type of a callable.

        However, the following **can** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` callables:

        - The number and content of lines yielded by a ``format_*``
          callable.
        - The content printed by a ``print_*`` callable.

    Parameters
    ----------
    cls: Type[:class:`~pretty.traceback.TracebackFormatter`]
        The formatter class to use. Defaults to
        :class:`~pretty.traceback.PrettyTracebackFormatter`.
    **kwargs
        Keyword arguments are passed to
        :meth:`TracebackFormatter.__init__ \
        <pretty.traceback.TracebackFormatter>`.


    :rtype: :class:`~pretty.traceback.TracebackFormatter`
    """

    formatter = cls and cls(*args, **kwargs) or PrettyTracebackFormatter(*args, **kwargs)

    traceback.extract_stack = formatter._extract_stack  # type: ignore
    traceback.extract_tb = formatter._extract_tb  # type: ignore
    traceback.format_exc = formatter._format_exc  # type: ignore
    traceback.format_exception = formatter._format_exception  # type: ignore
    traceback.format_exception_only = formatter._format_exception_only  # type: ignore
    traceback.format_list = formatter._format_list  # type: ignore
    traceback.format_stack = formatter._format_stack  # type: ignore
    traceback.format_tb = formatter._format_tb  # type: ignore
    traceback.print_exc = formatter._print_exc  # type: ignore
    traceback.print_exception = formatter._print_exception  # type: ignore
    traceback.print_last = formatter._print_last  # type: ignore
    traceback.print_list = formatter._print_list  # type: ignore
    traceback.print_stack = formatter._print_stack  # type: ignore
    traceback.print_tb = formatter._print_tb  # type: ignore
    traceback.walk_stack = formatter._walk_stack  # type: ignore
    traceback.walk_tb = formatter._walk_tb  # type: ignore

    def excepthook(*args):
        formatter.print_exception(*args)

    sys.excepthook = excepthook

    return formatter


__all__ = [  # pyright: ignore[reportUnsupportedDunderAll]
    *_formatter__all__,
    "hook",
]
