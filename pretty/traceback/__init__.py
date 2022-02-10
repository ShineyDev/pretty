import sys
import traceback

from pretty.traceback.formatter import *
from pretty.traceback.formatter import __all__ as _formatter__all__


def hook(cls=None, **kwargs):
    """
    Hooks pretty.traceback into the current Python session.

    .. note::

        You can set the :term:`PYTHONPRETTYTRACEBACK` environment
        variable to a :term:`truthy value <boolean value>` to hook
        pretty.traceback into all Python sessions.

    .. warning::

        This will replace attributes and functions in the
        :mod:`traceback` module with attributes and methods from the
        formatter.

        The following **cannot** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` methods:

        - Any parameter kind, name, order, or type of any function.
        - The return or yield type of any function.

        The following **can** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` methods:

        - The number and content of lines yielded by any ``format_*``
          function.
        - The content printed by any ``print_*`` function.

    Parameters
    ----------
    cls: Type[:class:`~pretty.traceback.TracebackFormatter`]
        The formatter class to use. Defaults to
        :class:`~pretty.traceback.PrettyTracebackFormatter`.
    **kwargs
        Keyword arguments are passed to
        :meth:`TracebackFormatter.__init__ \
        <pretty.traceback.TracebackFormatter>`.

    Returns
    -------
    :class:`~pretty.traceback.TracebackFormatter`
        The formatter.
    """

    formatter = cls and cls(**kwargs) or PrettyTracebackFormatter(**kwargs)

    # TODO: traceback.FrameSummary
    # TODO: traceback.StackSummary
    # TODO: traceback.TracebackException

    traceback.extract_stack = formatter._extract_stack
    traceback.extract_tb = formatter._extract_traceback
    traceback.format_exc = formatter._format_exc
    traceback.format_exception = formatter._format_exception
    traceback.format_exception_only = formatter._format_exception_only
    traceback.format_list = formatter._format_frames
    traceback.format_stack = formatter._format_stack
    traceback.format_tb = formatter._format_tb
    traceback.print_exc = formatter._print_exc
    traceback.print_exception = formatter._print_exception
    traceback.print_last = formatter._print_last
    traceback.print_list = formatter._print_frames
    traceback.print_stack = formatter._print_stack
    traceback.print_tb = formatter._print_tb
    traceback.walk_stack = formatter._walk_stack
    traceback.walk_tb = formatter._walk_traceback

    def excepthook(*args):
        formatter.print_exception(*args)

    sys.excepthook = excepthook

    return formatter


__all__ = [
    *_formatter__all__,
    "hook",
]
