from typing import TypeVar

from pretty.traceback.formatter import *


_F = TypeVar("_F", bound=TracebackFormatter)


def hook(cls: type[_F]=..., **kwargs) -> _F: ...
