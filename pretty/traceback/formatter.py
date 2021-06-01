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

    @utils.wrap(traceback.format_list)
    def _format_frames(self, extracted_list):
        return list(self.format_frames(extracted_list))

    @utils.wrap(traceback.print_list)
    def _write_frames(self, extracted_list, file=None):
        self.write_frames(extracted_list, file=file)

    @abc.abstractmethod
    def format_frames(self, frames):
        """
        |iter|

        Formats an iterable of traceback frames to be written to a
        file.

        This function is synonymous to :func:`traceback.format_list`.

        Parameters
        ----------
        frames
            An iterable of traceback frames.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

    def write_frames(self, frames, *, file=None):
        """
        Writes an iterable of traceback frames to a file.

        This function is synonymous to ``traceback.print_list()``.

        .. NOTE: traceback.print_list, while documented in the source,
                 is not documented on docs.python.org and thus cannot
                 be linked to by intersphinx.

        Parameters
        ----------
        frames
            An iterable of traceback frames.
        file
            The file to write to. Defaults to :data:`sys.stderr`.
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
