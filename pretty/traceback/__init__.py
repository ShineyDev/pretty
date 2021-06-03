import sys
import traceback

from pretty import utils
from pretty.traceback.formatter import TracebackFormatter
from pretty.traceback.formatter import DefaultTracebackFormatter
from pretty.traceback.formatter import PrettyTracebackFormatter


def hook(cls=None, **kwargs):
    """
    Hooks pretty.traceback into your Python session.

    .. note::

        Set the :term:`PYTHONPRETTYTRACEBACK` environment variable to a
        :term:`truthy value <boolean value>` to hook pretty.traceback
        into all future Python sessions.

    .. warning::

        This will replace attributes and functions in the
        :mod:`traceback` module with attributes and methods from the
        formatter.
        
        .. TODO: , falling back to :mod:`traceback` methods if the
           formatter fails.

        The following **cannot** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` methods:

        - The parameter kind, name, order, or type of any function.
        - The return or yield type of any function.

        The following **can** change when a
        :class:`~pretty.traceback.TracebackFormatter` subclass
        overrides built-in :mod:`traceback` methods:

        - The number and content of lines yielded by any ``format_*``
          method.

    Parameters
    ----------
    cls: Type[:class:`~pretty.traceback.TracebackFormatter`]
        The formatter to use. Defaults to
        :class:`~pretty.traceback.PrettyTracebackFormatter`.
    **kwargs
        Keyword arguments are passed to
        :meth:`TracebackFormatter.__init__ \
        <pretty.traceback.TracebackFormatter>`.

    Returns
    -------
    :class:`~pretty.traceback.TracebackFormatter`
        The formatter hooked into your Python session.
    """

    formatter = cls and cls(**kwargs) or PrettyTracebackFormatter(**kwargs)

    # TODO: traceback.clear_frames = ...
    traceback.extract_stack = formatter._extract_stack
    traceback.extract_tb = formatter._extract_traceback
    traceback.format_exc = formatter._format_current_exception
    traceback.format_exception = formatter._format_exception
    traceback.format_exception_only = formatter._format_exception_only
    traceback.format_list = formatter._format_frames
    traceback.format_stack = formatter._format_stack
    traceback.format_tb = formatter._format_traceback
    traceback.print_exc = formatter._print_current_exception
    traceback.print_exception = formatter._print_exception
    traceback.print_last = formatter._print_last_exception
    traceback.print_list = formatter._print_frames
    traceback.print_stack = formatter._print_stack
    traceback.print_tb = formatter._print_traceback

    if isinstance(formatter, DefaultTracebackFormatter):
        traceback._cause_message = formatter.cause_message
        traceback._context_message = formatter.context_message

    if sys.version_info >= (3, 10):
        traceback._parse_value_tb = formatter._extract_value_traceback

    # TODO: traceback._format_final_exc_line = ...
    traceback._some_str = formatter._try_str

    def excepthook(*args):
        formatter.print_exception(*args)

    sys.excepthook = excepthook

    return formatter


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
    "hook",
]
