import abc
import sys
import traceback

from pretty import utils


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.
    """

    def __init__(self, *, theme):
        self.theme = theme

    @utils.wrap(traceback.print_list)
    def _write_frames(self, extracted_list, file=None):
        self.write_frames(extracted_list, file=file)

    def write_frames(self, frames, *, file=None):
        """
        Writes an iterable of traceback frames.

        This function is synonymous to ``traceback.print_list()``.

        .. NOTE: traceback.print_list, while documented in the source,
                 is not documented on docs.python.org and thus cannot
                 be linked to by intersphinx.

        Parameters
        ----------
        frames: Iterable[:class:`~pretty.traceback.Frame`]
            An iterable of traceback frames.
        file
            The file to write to.
        """

        print("".join(self.format_frames(frames)), end="", file=file or sys.stderr)


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.
    """

    ...


class PrettyTracebackFormatter(DefaultTracebackFormatter):
    """
    A pretty :class:`.TracebackFormatter`.
    """

    ...


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
