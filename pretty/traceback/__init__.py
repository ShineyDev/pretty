import sys
import traceback

from pretty import utils
from pretty.traceback.formatter import TracebackFormatter
from pretty.traceback.formatter import DefaultTracebackFormatter
from pretty.traceback.formatter import PrettyTracebackFormatter


def hook(cls=None, *, override_builtin=None, override_hook=None, **kwargs):
    """
    Hooks pretty.traceback into your Python session.

    Parameters
    ----------
    cls: Type[:class:`~pretty.traceback.TracebackFormatter`]
        The formatter to use. Defaults to
        :class:`~pretty.traceback.PrettyTracebackFormatter`.
    override_builtin: :class:`bool`
        Whether to override :mod:`traceback`'s methods with methods
        from the formatter.

        .. tip::

            Providing this parameter will override the
            :term:`corresponding environment variable \
            <PYTHONPRETTYTRACEBACKOVERRIDEBUILTIN>`, which defaults to
            ``False``.

        .. note::

            The following **cannot** change when a
            :class:`TracebackFormatter` subclass overrides the builtin
            :mod:`traceback` methods.

            - The parameter kind, name, order, or type of any function.
            - The return or yield type of any function.

        .. warning::

            The following **can** change when a
            :class:`TracebackFormatter` subclass overrides the builtin
            :mod:`traceback` methods.

            - The number and content of lines yielded by any
              ``format_*`` function.
    override_hook: :class:`bool`
        Whether to override :func:`sys.excepthook <sys.excepthook>`.

        .. tip::

            Providing this parameter will override the
            :term:`corresponding environment variable \
            <PYTHONPRETTYTRACEBACKOVERRIDEHOOK>`, which defaults to
            ``True``.
    **kwargs
        Additional keyword arguments are passed to
        :meth:`TracebackFormatter.__init__ \
        <pretty.traceback.TracebackFormatter>`.

    Returns
    -------
    :class:`~pretty.traceback.TracebackFormatter`
        The formatter hooked into your Python session.
    """

    formatter = cls and cls(**kwargs) or PrettyTracebackFormatter(**kwargs)

    if override_builtin is None:
        override_builtin = utils.environment_to_bool(utils._env_traceback_override_builtin, False)

    if override_builtin:
        traceback.extract_tb = formatter._extract_traceback
        traceback.format_exception = formatter._format_exception
        traceback.format_exception_only = formatter._format_exception_only
        traceback.format_list = formatter._format_frames
        traceback.format_tb = formatter._format_traceback
        traceback.print_exception = formatter._write_exception
        traceback.print_list = formatter._write_frames
        traceback.print_tb = formatter._write_traceback

        if isinstance(formatter, DefaultTracebackFormatter):
            traceback._cause_message = formatter.cause_message
            traceback._context_message = formatter.context_message

        if sys.version_info >= (3, 10):
            traceback._parse_value_tb = formatter._extract_value_traceback

        # TODO: traceback._format_final_exc_line = ...
        traceback._some_str = formatter._try_str

    if override_hook is None:
        override_hook = utils.environment_to_bool(utils._env_traceback_override_hook, True)

    if override_hook:
        def excepthook(*args):
            formatter.write_exception(*args)

        sys.excepthook = excepthook

    return formatter


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
    "hook",
]
