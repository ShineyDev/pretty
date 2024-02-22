from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

import sys


PY_312: Final[bool] = sys.version_info >= (3, 12, 0)

SUPPORTS_SYSLASTEXC = PY_312  # sys.last_exc


__all__ = [
    "PY_312",
    "SUPPORTS_SYSLASTEXC",
]
