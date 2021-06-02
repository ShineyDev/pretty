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

    @utils.wrap(traceback.extract_tb)
    def _extract_traceback(self, tb, limit=None):
        return traceback.StackSummary(self.extract_frames(tb, limit=limit))

    @utils.wrap(traceback.format_list)
    def _format_frames(self, extracted_list):
        return list(self.format_frames(extracted_list))

    @utils.wrap(traceback.format_tb)
    def _format_traceback(self, tb, limit=None):
        return list(self.format_traceback(tb, limit=limit))

    @utils.wrap(traceback.print_list)
    def _write_frames(self, extracted_list, file=None):
        self.write_frames(extracted_list, file=file)

    @utils.wrap(traceback.print_tb)
    def _write_traceback(self, tb, limit=None, file=None):
        self.write_traceback(tb, file=file, limit=limit)

    @abc.abstractmethod
    def extract_frames(self, obj, *, limit=None):
        """
        |iter|

        Extracts frames from a :data:`~types.FrameType` or
        :class:`~types.TracebackType`.

        This function is synonymous to both
        :func:`traceback.extract_stack` and
        :func:`traceback.extract_tb`.

        Parameters
        ----------
        obj: Union[:data:`~types.FrameType`, \
                   :class:`~types.TracebackType`]
            A frame or traceback.
        limit: :class:`int`
            The maximum number of frames to extract.

        Yields
        ------
        Any
            Frames to be formatted.
        """

        raise NotImplementedError

    @abc.abstractmethod
    def format_frames(self, frames):
        """
        |iter|

        Formats an iterable of frames to be written to a file.

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

    def format_traceback(self, traceback, *, limit=None):
        """
        |iter|

        Formats a traceback to be written to a file.

        This function is synonymous to :func:`traceback.format_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.
        limit: :class:`int`
            The maximum number of frames to format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        yield from self.format_frames(self.extract_frames(traceback, limit=limit))

    def write_frames(self, frames, *, file=None):
        """
        Writes an iterable of frames to a file.

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

    def write_traceback(self, traceback, *, file=None, limit=None):
        """
        Writes a traceback to a file.

        This function is synonymous to :func:`traceback.print_tb`.

        Parameters
        ----------
        traceback: :class:`~types.TracebackType`
            A traceback.
        file
            The file to write to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to format and write.
        """

        print("".join(self.format_traceback(traceback, limit=limit)), end="", file=file or sys.stderr)


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.
    """

    cause_message = traceback._cause_message


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
