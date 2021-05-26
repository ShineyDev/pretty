from typing import Callable, Type

from types import TracebackType

from pretty.formatter import Formatter as Formatter
from pretty.formatter import TracebackFormatter as TracebackFormatter
from pretty.formatter import DefaultFormatter as DefaultFormatter


def is_hooked() -> bool: ...
def create_excepthook(formatter: Formatter) -> Callable[[Type[BaseException], BaseException, TracebackType], None]: ...
def hook(cls: Type[Formatter]=..., *, override_hook: bool=..., override_traceback: bool=..., **kwargs) -> None: ...
