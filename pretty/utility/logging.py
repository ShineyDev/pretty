from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsWrite
    from typing_extensions import Self

import logging
import sys


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
    "CurrentStandardErrorStreamHandler",
]
