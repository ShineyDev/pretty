from typing import TypeVar

from pretty.traceback.formatter import TracebackFormatter as TracebackFormatter
from pretty.traceback.formatter import DefaultTracebackFormatter as DefaultTracebackFormatter
from pretty.traceback.formatter import PrettyTracebackFormatter as PrettyTracebackFormatter


T = TypeVar("T", bound=TracebackFormatter)


def hook(cls: type[T]=..., *, override_builtin: bool=..., override_hook: bool=..., **kwargs) -> T: ...
