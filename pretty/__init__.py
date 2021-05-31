import collections
import sys
import traceback

from pretty.formatter import (
    Formatter,
    TracebackFormatter,
    DefaultFormatter,
)


_VersionInfo = collections.namedtuple("_VersionInfo", "major minor micro release serial")

version = "1.0.0"
version_info = _VersionInfo(1, 0, 0, "final", 0)


def is_hooked():
    """
    Returns
    -------
    :class:`bool`
        Whether pretty, or another module, is hooked into :attr:`sys.excepthook`.
    """

    return sys.excepthook is not sys.__excepthook__


def create_excepthook(formatter):
    """
    Creates a callable to replace :attr:`sys.excepthook` from a
    :class:`~pretty.Formatter`.

    Parameters
    ----------
    formatter: :class:`~pretty.Formatter`
        The formatter to use.

    Returns
    -------
    Callable[[Type[:class:`BaseException`], :class:`BaseException`, :class:`~types.TracebackType`], ``None``]
        An :attr:`sys.excepthook` callable.
    """

    def excepthook(*args):
        print("".join(formatter.format_exception(*args)).strip())

    return excepthook


def hook(cls=DefaultFormatter, *, override_hook=False, override_traceback=False, **kwargs):
    """
    Hooks pretty into your Python session.

    Parameters
    ----------
    cls: Type[:class:`~pretty.Formatter`]
        The formatter to use.

        Defaults to :class:`~pretty.DefaultFormatter`.
    override_hook: :class:`bool`
        Whether to override an already-overridden
        :attr:`sys.excepthook`.
    override_traceback: :class:`bool`
        Whether to override :mod:`traceback`'s ``format_*`` methods
        with methods from the formatter.

        Useful for overriding tracebacks printed by strange third-party
        modules. But, probably don't ever use this.
    **kwargs
        Additional keyword arguments are passed to
        :meth:`Formatter.__init__ <pretty.Formatter.__init__>`.
    """

    formatter = cls(**kwargs)

    if override_traceback:
        traceback.format_exc = formatter.format_exc
        traceback.format_exception = formatter.format_exception
        traceback.format_exception_only = formatter.format_exception_only
        traceback.format_list = formatter.format_list
        traceback.format_stack = formatter.format_stack
        traceback.format_tb = formatter.format_traceback

    if override_hook or not is_hooked():
        sys.excepthook = create_excepthook(formatter)
