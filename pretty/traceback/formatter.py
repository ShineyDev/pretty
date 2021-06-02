import abc
import sys
import traceback

from pretty import utils


_sentinel = object()


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.

    Attributes
    ----------
    theme: :class:`dict`
        A theme.
    """

    def __init__(self, *, theme):
        self.theme = theme

    # region public methods

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

        yield

    @abc.abstractmethod
    def format_exception(self, type, value, traceback, *, chain=True, limit=None):
        """
        |iter|

        Formats an exception to be written to a file.

        This function is synonymous to
        :func:`traceback.format_exception`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_exception_only(self, type, value):
        """
        |iter|

        Formats an exception to be written to a file.

        This function is synonymous to
        :func:`traceback.format_exception_only`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        raise NotImplementedError

        yield

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

        yield

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
            The maximum number of frames to extract and format.

        Yields
        ------
        :class:`str`
            Lines to be written.
        """

        yield from self.format_frames(self.extract_frames(traceback, limit=limit))

    def write_exception(self, type, value, traceback, *, chain=True, file=None, limit=None):
        """
        Writes an exception to a file.

        This function is synonymous to
        :func:`traceback.print_exception`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        file
            The file to write to. Defaults to :data:`sys.stderr`.
        limit: :class:`int`
            The maximum number of frames to extract, format, and write.
        """

        print("".join(self.format_exception(type, value, traceback, chain=chain, limit=limit)), end="", file=file or sys.stderr)

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
            The maximum number of frames to extract, format, and write.
        """

        print("".join(self.format_traceback(traceback, limit=limit)), end="", file=file or sys.stderr)

    # endregion
    # region private methods

    def _extract_value_traceback(self, type, value, traceback):
        if (value is _sentinel) != (traceback is _sentinel):
            raise ValueError("Both or neither of value and tb must be given")
        elif value is _sentinel:
            if type is None:
                return None, None
            else:
                return type, type.__traceback__
        else:
            return value, traceback

    @utils.wrap(traceback.extract_tb)
    def _extract_traceback(self, tb, limit=None):
        return traceback.StackSummary(self.extract_frames(tb, limit=limit))

    if sys.version_info >= (3, 10):
        @utils.wrap(traceback.format_exception)
        def _format_exception(self, exc, value=_sentinel, tb=_sentinel, limit=None, chain=True):
            value, tb = self._extract_value_traceback(exc, value, tb)
            exc = type(value)

            return list(self.format_exception(exc, value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, exc, value=_sentinel):
            value, _ = self._extract_value_traceback(exc, value, None)
            exc = type(value)

            return list(self.format_exception_only(exc, value))
    else:
        @utils.wrap(traceback.format_exception)
        def _format_exception(self, etype, value, tb, limit=None, chain=True):
            return list(self.format_exception(type(value), value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, etype, value):
            return list(self.format_exception_only(type(value), value))

    @utils.wrap(traceback.format_list)
    def _format_frames(self, extracted_list):
        return list(self.format_frames(extracted_list))

    @utils.wrap(traceback.format_tb)
    def _format_traceback(self, tb, limit=None):
        return list(self.format_traceback(tb, limit=limit))

    if sys.version_info >= (3, 10):
        @utils.wrap(traceback.print_exception)
        def _write_exception(self, exc, value=_sentinel, tb=_sentinel, limit=None, file=None, chain=True):
            value, tb = self._extract_value_traceback(exc, value, tb)
            exc = type(value)

            self.write_exception(exc, value, tb, chain=chain, file=file, limit=limit)
    else:
        @utils.wrap(traceback.print_exception)
        def _write_exception(self, etype, value, tb, limit=None, file=None, chain=True):
            self.write_exception(type(value), value, tb, chain=chain, file=file, limit=limit)

    @utils.wrap(traceback.print_list)
    def _write_frames(self, extracted_list, file=None):
        self.write_frames(extracted_list, file=file)

    @utils.wrap(traceback.print_tb)
    def _write_traceback(self, tb, limit=None, file=None):
        self.write_traceback(tb, file=file, limit=limit)

    # endregion


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.

    Attributes
    ----------
    cause_message: :class:`str`
        The message yielded before an exception's ``__cause__``.
    context_message: :class:`str`
        The message yielded before an exception's ``__context__``.
    """

    cause_message = traceback._cause_message
    context_message = traceback._context_message


class PrettyTracebackFormatter(DefaultTracebackFormatter):
    """
    A pretty :class:`.TracebackFormatter`.

    Attributes
    ----------
    cause_message: :class:`str`
        The message yielded before an exception's ``__cause__``.
    context_message: :class:`str`
        The message yielded before an exception's ``__context__``.
    """

    ...


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
