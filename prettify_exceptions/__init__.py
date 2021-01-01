"""
/prettify_exceptions/__init__.py

    Copyright (c) 2020 ShineyDev

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys
import traceback

from prettify_exceptions.formatter import (
    Formatter,
    TracebackFormatter,
    DefaultFormatter,
)


def is_hooked():
    """
    Returns
    -------
    :class:`bool`
        Whether prettify, or another module, is hooked into :attr:`sys.excepthook`.
    """

    return sys.excepthook is not sys.__excepthook__


def create_excepthook(formatter):
    """
    Creates a callable to replace :attr:`sys.excepthook` from a
    :class:`~prettify_exceptions.Formatter`.

    Parameters
    ----------
    formatter: :class:`~prettify_exceptions.Formatter`
        The formatter to use.

    Returns
    -------
    Callable[[Type[:class:`BaseException`], :class:`BaseException`, :class:`~types.TracebackType`], ``None``]
        An :attr:`sys.excepthook` callable.
    """

    def excepthook(*args):
        print("".join(formatter.format_exception(*args)).strip())

    return excepthook


def hook(
    cls=DefaultFormatter,
    *,
    override_hook=False,
    override_traceback=False,
    **kwargs
):
    """
    Hooks prettify into your Python session.

    Parameters
    ----------
    cls: Type[:class:`~prettify_exceptions.Formatter`]
        The formatter to use.

        Defaults to :class:`~prettify_exceptions.DefaultFormatter`.
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
        :meth:`Formatter.__init__ <prettify_exceptions.Formatter.__init__>`.
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
