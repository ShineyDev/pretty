from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsWrite, OptExcInfo
    from logging import LogRecord
    from typing_extensions import Self

import logging
import sys

from pretty.utility.version import SUPPORTS_SYSLASTEXC


class MinimalExceptionFormatter(logging.Formatter):
    """
    |internal|

    TODO
    """

    def format(
        self: Self,
        record: LogRecord,
        /,
    ) -> str:
        # NOTE: let the base formatter handle setting attributes
        _ = super().format(record)

        s = self.formatMessage(record)

        if record.exc_text:
            # NOTE: we don't want any wrapped lines
            # if s[-1:] != "\n":
            #     s = s + "\n"

            s += record.exc_text

        if record.stack_info:
            # NOTE: we don't want any wrapped lines
            # if s[-1:] != "\n":
            #     s = s + "\n"

            s += self.formatStack(record.stack_info)

        return s

    def formatException(
        self: Self,
        exc_info: OptExcInfo,
        /,
    ) -> str:
        if hasattr(sys, "last_exc") or hasattr(sys, "last_value"):
            return ""

        exc_type, exc_value, exc_traceback = exc_info

        if SUPPORTS_SYSLASTEXC:
            sys.last_exc = exc_value  # type: ignore  # sys.last_exc does exist

        # NOTE: deprecated in Python 3.12, but set anyway
        sys.last_type = exc_type
        sys.last_value = exc_value
        sys.last_traceback = exc_traceback

        if SUPPORTS_SYSLASTEXC:
            return " (See sys.last_exc)"
        else:
            return " (See sys.last_value)"


class CurrentStandardErrorStreamHandler(logging.StreamHandler):
    """
    |internal|

    TODO
    """

    def __init__(
        self: Self,
        /,
    ) -> None:
        """
        Initialize the handler.
        """  # NOTE: this is required

        super(logging.StreamHandler, self).__init__(logging.NOTSET)

    @property
    def stream(
        self: Self,
        /,
    ) -> SupportsWrite[str]:
        return sys.stderr


__all__ = [
    "MinimalExceptionFormatter",
    "CurrentStandardErrorStreamHandler",
]
