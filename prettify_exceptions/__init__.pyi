from typing import Callable, Type

from types import TracebackType

from prettify_exceptions.formatter import Formatter as Formatter
from prettify_exceptions.formatter import TracebackFormatter as TracebackFormatter
from prettify_exceptions.formatter import DefaultFormatter as DefaultFormatter


def is_hooked() -> bool: ...
def create_excepthook(formatter: Formatter) -> Callable[[Type[BaseException], BaseException, TracebackType], None]: ...
def hook(cls: Type[Formatter]=..., *, override_hook: bool=..., override_traceback: bool=..., **kwargs) -> None: ...
