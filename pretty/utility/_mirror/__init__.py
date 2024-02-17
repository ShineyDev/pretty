"""
utility: A Python package with utilities I use in several of my other projects.
"""

from __future__ import annotations
from typing import NamedTuple

from .cache import *
from .cache import __all__ as _cache__all__
from .typing import *
from .typing import __all__ as _typing__all__
from .version import *
from .version import __all__ as _version__all__
from .warning import *
from .warning import __all__ as _warning__all__
from .wrapper import *
from .wrapper import __all__ as _wrapper__all__


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


version: str = "0.1.0a"
version_info: _VersionInfo = _VersionInfo(0, 1, 0, "alpha", 0)


__all__ = [  # pyright: ignore[reportUnsupportedDunderAll]
    *_cache__all__,
    *_typing__all__,
    *_version__all__,
    *_warning__all__,
    *_wrapper__all__,
]
