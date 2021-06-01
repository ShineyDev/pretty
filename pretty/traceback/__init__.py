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

            - The parameter kind, name, or type of any function.
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
        traceback.extract_stack = ...
        traceback.extract_tb = ...
        traceback.format_exc = ...
        traceback.format_exception = ...
        traceback.format_exception_only = ...
        traceback.format_list = ...
        traceback.format_stack = ...
        traceback.format_tb = ...
        traceback.print_exc = ...
        traceback.print_exception = ...
        traceback.print_last = ...
        traceback.print_list = ...
        traceback.print_stack = ...
        traceback.print_tb = ...
        traceback.walk_stack = ...
        traceback.walk_tb = ...

    if override_hook is None:
        override_hook = utils.environment_to_bool(utils._env_traceback_override_hook, True)

    if override_hook:
        def excepthook(*args):
            print("".join(formatter.format_exception(*args)).strip())

        sys.excepthook = excepthook

    return formatter


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
    "hook",
]
