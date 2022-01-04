from typing import NamedTuple

from pretty import utils as utils
from pretty import traceback as traceback


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int

version: str = ...
version_info: _VersionInfo = ...
