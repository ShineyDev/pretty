import abc
import itertools
import sys
import textwrap
import traceback
import types

from pretty import utils


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.
    """

    __slots__ = ()

    @abc.abstractmethod
    def format_exception(self, type, value):
        """
        |iter|

        Formats an exception.

        This function is synonymous to
        :func:`traceback.format_exception_only`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_frame(self, frame):
        """
        |iter|

        Formats a frame.

        This function is synonymous to
        ``traceback.StackSummary.format_frame_summary``.

        .. NOTE: traceback.StackSummary.format_frame_summary, while
                 documented in the source, is not documented on
                 docs.python.org and thus cannot be linked to by
                 intersphinx.

        Parameters
        ----------
        frame: Tuple[ \
                   Union[ \
                       :data:`~types.FrameType`, \
                       :class:`~traceback.FrameSummary` \
                   ], \
                   Tuple[ \
                       :class:`int`, \
                       Optional[:class:`int`], \
                       Optional[:class:`int`], \
                       Optional[:class:`int`] \
                   ] \
               ]
            A frame.
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_stack(self, stack):
        """
        |iter|

        Formats a stack.

        This function is synonymous to :func:`traceback.format_list`.

        Parameters
        ----------
        stack: Iterable[ \
                   Tuple[ \
                       Union[ \
                           :data:`~types.FrameType`, \
                           :class:`~traceback.FrameSummary` \
                       ], \
                       Tuple[ \
                           :class:`int`, \
                           Optional[:class:`int`], \
                           Optional[:class:`int`], \
                           Optional[:class:`int`] \
                       ] \
                   ] \
               ]
            A stack of frames.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_traceback(self, type, value, traceback, *, chain=None, limit=None):
        """
        |iter|

        Formats a traceback.

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
            The maximum number of frames to extract.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    def print_exception(self, type, value, *, stream=None):
        """
        Prints an exception to :data:`~sys.stderr`.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_exception(type, value, stream=stream or sys.stderr)

    def print_frame(self, frame, *, stream=None):
        """
        Prints a frame to :data:`~sys.stderr`.

        Parameters
        ----------
        frame: Tuple[ \
                   Union[ \
                       :data:`~types.FrameType`, \
                       :class:`~traceback.FrameSummary` \
                   ], \
                   Tuple[ \
                       :class:`int`, \
                       Optional[:class:`int`], \
                       Optional[:class:`int`], \
                       Optional[:class:`int`] \
                   ] \
               ]
            A frame.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_frame(frame, stream=stream or sys.stderr)

    def print_stack(self, stack, *, stream=None):
        """
        Prints a stack to :data:`~sys.stderr`.

        This function is synonymous to ``traceback.print_list()``.

        .. NOTE: traceback.print_list, while documented in the source,
                 is not documented on docs.python.org and thus cannot
                 be linked to by intersphinx.

        Parameters
        ----------
        stack: Iterable[ \
                   Tuple[ \
                       Union[ \
                           :data:`~types.FrameType`, \
                           :class:`~traceback.FrameSummary` \
                       ], \
                       Tuple[ \
                           :class:`int`, \
                           Optional[:class:`int`], \
                           Optional[:class:`int`], \
                           Optional[:class:`int`] \
                       ] \
                   ] \
               ]
            A stack of frames.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_stack(stack, stream=stream or sys.stderr)

    def print_traceback(self, type, value, traceback, *, chain=None, limit=None, stream=None):
        """
        Prints a traceback to :data:`~sys.stderr`.

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
        limit: :class:`int`
            The maximum number of frames to extract.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_traceback(type, value, traceback, chain=chain, limit=limit, stream=stream or sys.stderr)

    @abc.abstractmethod
    def walk_stack(self, obj, *, limit):
        """
        |iter|

        Walks a stack.

        This function is synonymous to both
        :func:`traceback.walk_stack` and :func:`traceback.walk_tb`.

        Parameters
        ----------
        obj: Union[:data:`~types.FrameType`, :class:`~types.TracebackType`]
            A frame or traceback.
        limit: :class:`int`
            The maximum number of frames to extract.


        :yields: Tuple[ \
                     :data:`~types.FrameType`, \
                     Tuple[ \
                         :class:`int`,
                         Optional[:class:`int`], \
                         Optional[:class:`int`], \
                         Optional[:class:`int`] \
                     ] \
                 ]
        """

        raise NotImplementedError

        yield

    def write_exception(self, type, value, *, stream):
        """
        Writes an exception to a stream.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        stream: :func:`TextIO <open>`
            The stream to write to.
        """

        stream.write("".join(self.format_exception(type, value)))

    def write_frame(self, frame, *, stream=None):
        """
        Writes a frame to a stream.

        Parameters
        ----------
        frame: Tuple[ \
                   Union[ \
                       :data:`~types.FrameType`, \
                       :class:`~traceback.FrameSummary` \
                   ], \
                   Tuple[ \
                       :class:`int`, \
                       Optional[:class:`int`], \
                       Optional[:class:`int`], \
                       Optional[:class:`int`] \
                   ] \
               ]
            A frame.
        stream: :func:`TextIO <open>`
            The stream to write to.
        """

        stream.write("".join(self.format_frame(frame)))

    def write_stack(self, stack, *, stream):
        """
        Writes a stack to a stream.

        Parameters
        ----------
        stack: Iterable[ \
                   Tuple[ \
                       Union[ \
                           :data:`~types.FrameType`, \
                           :class:`~traceback.FrameSummary` \
                       ], \
                       Tuple[ \
                           :class:`int`, \
                           Optional[:class:`int`], \
                           Optional[:class:`int`], \
                           Optional[:class:`int`] \
                       ] \
                   ] \
               ]
            A stack of frames.
        stream: :func:`TextIO <open>`
            The stream to write to.
        """

        stream.write("".join(self.format_stack(stack)))

    def write_traceback(self, type, value, traceback, *, stream, chain=None, limit=None):
        """
        Writes a traceback to a stream.

        Parameters
        ----------
        type: Type[:class:`BaseException`]
            An exception type.
        value: :class:`BaseException`
            An exception.
        traceback: :class:`~types.TracebackType`
            A traceback.
        stream: :func:`TextIO <open>`
            The stream to write to.
        chain: :class:`bool`
            Whether to follow the traceback tree.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        stream.write("".join(self.format_traceback(type, value, traceback, chain=chain, limit=limit)))

    @utils.wrap(traceback.extract_stack)
    def _extract_stack(self, f=None, limit=None):
        generator = self.walk_stack(f or sys._getframe().f_back, limit=limit)

        if sys.version_info >= (3, 11):
            extract = traceback.StackSummary._extract_from_extended_frame_gen
        else:
            extract = traceback.StackSummary.extract

            def generator_function():
                for (frame, position) in generator:
                    yield frame, position[0]

            generator = generator_function()

        stack = extract(generator)
        stack.reverse()

        return stack

    @utils.wrap(traceback.extract_tb)
    def _extract_tb(self, tb, limit=None):
        generator = self.walk_stack(tb, limit=limit)

        if sys.version_info >= (3, 11):
            extract = traceback.StackSummary._extract_from_extended_frame_gen
        else:
            extract = traceback.StackSummary.extract

            def generator_function():
                for (frame, position) in generator:
                    yield frame, position[0]

            generator = generator_function()

        stack = extract(generator)

        return stack

    @utils.wrap(traceback.format_exc)
    def _format_exc(self, limit=None, chain=True):
        _, value, traceback = sys.exc_info()

        return "".join(self.format_traceback(value.__class__, value, traceback, chain=chain, limit=limit))

    if sys.version_info >= (3, 10):

        @utils.wrap(traceback.format_exception)
        def _format_exception(self, exc, value=traceback._sentinel, tb=traceback._sentinel, limit=None, chain=True):
            if (value is traceback._sentinel) != (tb is traceback._sentinel):
                raise ValueError("Both or neither of value and tb must be given")
            elif value is traceback._sentinel:
                if exc is None:
                    value, tb = None, None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {exc.__class__.__name__} found")

                    value, tb = exc, exc.__traceback__

            return list(self.format_traceback(value.__class__, value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, exc, value=traceback._sentinel):
            if value is traceback._sentinel:
                if exc is None:
                    value = None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {exc.__class__.__name__} found")

                    value = exc

            return list(self.format_exception(value.__class__, value))

    else:

        @utils.wrap(traceback.format_exception)
        def _format_exception(self, etype, value, tb, limit=None, chain=True):
            return list(self.format_traceback(value.__class__, value, tb, chain=chain, limit=limit))

        @utils.wrap(traceback.format_exception_only)
        def _format_exception_only(self, etype, value):
            return list(self.format_exception(value.__class__, value))

    @utils.wrap(traceback.format_list)
    def _format_list(self, extracted_list):
        return list(self.format_stack((traceback.FrameSummary(filename, lineno, name, line=line), (lineno, None, None, None)) for (filename, lineno, name, line) in extracted_list))

    @utils.wrap(traceback.format_stack)
    def _format_stack(self, f=None, limit=None):
        return list(self.format_stack(self.walk_stack(f or sys._getframe().f_back, limit=limit)))

    @utils.wrap(traceback.format_tb)
    def _format_tb(self, tb, limit=None):
        return list(self.format_stack(self.walk_stack(tb, limit=limit)))

    @utils.wrap(traceback.print_exc)
    def _print_exc(self, limit=None, file=None, chain=True):
        _, value, traceback = sys.exc_info()

        self.print_traceback(value.__class__, value, traceback, chain=chain, limit=limit, stream=file)

    if sys.version_info >= (3, 10):

        @utils.wrap(traceback.print_exception)
        def _print_exception(self, exc, value=traceback._sentinel, tb=traceback._sentinel, limit=None, file=None, chain=True):
            if (value is traceback._sentinel) != (tb is traceback._sentinel):
                raise ValueError("Both or neither of value and tb must be given")
            elif value is traceback._sentinel:
                if exc is None:
                    value, tb = None, None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {exc.__class__.__name__} found")

                    value, tb = exc, exc.__traceback__

            self.print_traceback(value.__class__, value, tb, chain=chain, limit=limit, stream=file)

    else:

        @utils.wrap(traceback.print_exception)
        def _print_exception(self, etype, value, tb, limit=None, file=None, chain=True):
            self.print_traceback(value.__class__, value, tb, chain=chain, limit=limit, stream=file)

    @utils.wrap(traceback.print_last)
    def _print_last(self, limit=None, file=None, chain=True):
        if not hasattr(sys, "last_type"):
            raise ValueError("no last exception")

        value, traceback = sys.last_value, sys.last_traceback

        self.print_traceback(value.__class__, value, traceback, chain=chain, limit=limit, stream=file)

    @utils.wrap(traceback.print_list)
    def _print_list(self, extracted_list, file=None):
        self.print_stack(((traceback.FrameSummary(filename, lineno, name, line=line), (lineno, None, None, None)) for (filename, lineno, name, line) in extracted_list), stream=file)

    @utils.wrap(traceback.print_stack)
    def _print_stack(self, f=None, limit=None, file=None):
        self.print_stack(self.walk_stack(f or sys._getframe().f_back, limit=limit), stream=file)

    @utils.wrap(traceback.print_tb)
    def _print_tb(self, tb, limit=None, file=None):
        self.print_stack(self.walk_stack(tb, limit=limit), stream=file)

    @utils.wrap(traceback.walk_stack)
    def _walk_stack(self, f):
        if sys.version_info >= (3, 11):
            f = f or sys._getframe().f_back.f_back.f_back.f_back
        else:
            f = f or sys._getframe().f_back.f_back

        for frame, position in self.walk_stack(f):
            yield frame, position[0]

    @utils.wrap(traceback.walk_tb)
    def _walk_tb(self, tb):
        for frame, position in self.walk_stack(tb):
            yield frame, position[0]


class DefaultTracebackFormatter(TracebackFormatter):
    """
    A :class:`.TracebackFormatter` with reimplementations of the
    :mod:`traceback` module.

    Attributes
    ----------
    cause_header: :class:`str`
        The message yielded after an exception's cause.
    context_header: :class:`str`
        The message yielded after an exception's context.
    recursion_cutoff: :class:`int`
        The number of the same frame to display before instead
        displaying a recursion message.
    recursion_message_format: :class:`str`
        The format for the message yielded in place of recursive
        frames.
    traceback_header: :class:`str`
        The message yielded before an exception's traceback.
    """

    __slots__ = ()

    cause_header = "The above exception was the direct cause of the following exception:"
    context_header = "During handling of the above exception, another exception occurred:"
    recursion_cutoff = 3
    recursion_message_format = "[Previous line repeated {times} more time{'' if times == 1 else 's'}]"
    traceback_header = "Traceback (most recent call last):"

    def format_exception(self, type, value):
        type_name = utils.try_name(type)
        value_str = utils.try_str(value)

        if value_str:
            line = f"{type_name}: {value_str}\n"
        else:
            line = f"{type_name}\n"

        yield line

    def format_stack(self, stack):
        last_filename = None
        last_lineno = None
        last_name = None
        recursion_times = 0

        for (frame, position) in stack:
            if isinstance(frame, types.FrameType):
                current_filename = frame.f_code.co_filename
                current_name = frame.f_code.co_name
            else:
                current_filename = frame.filename
                current_name = frame.name

            current_lineno = position[0]

            if current_filename != last_filename or current_lineno != last_lineno or current_name != last_name:
                if recursion_times > self.recursion_cutoff:
                    yield utils.format(self.recursion_message_format, times=recursion_times - self.recursion_cutoff)

                last_filename = current_filename
                last_lineno = current_lineno
                last_name = current_name
                recursion_times = 0

            recursion_times += 1

            if recursion_times > self.recursion_cutoff:
                continue

            yield from self.format_frame((frame, position))

        if recursion_times > self.recursion_cutoff:
            yield utils.format(self.recursion_message_format, times=recursion_times - self.recursion_cutoff)

    def format_traceback(self, type, value, traceback, *, chain=None, limit=None, seen=None):
        if chain is None:
            chain = True

        if chain and value is not None:
            seen = seen or set()
            seen.add(id(value))

            cause = value.__cause__

            if cause is not None and id(cause) not in seen:
                yield from self.format_traceback(cause.__class__, cause, cause.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.cause_header

            context = value.__context__
            context_suppressed = value.__suppress_context__

            if cause is None and context is not None and not context_suppressed and id(context) not in seen:
                yield from self.format_traceback(context.__class__, context, context.__traceback__, chain=chain, limit=limit, seen=seen)
                yield self.context_header

        if traceback is not None:
            yield self.traceback_header

            for line in self.format_stack(self.walk_stack(traceback, limit=limit)):
                yield textwrap.indent(line, "  ")

        yield from self.format_exception(type, value)

    def walk_stack(self, obj, *, limit=None):
        if isinstance(obj, types.TracebackType):
            limit = limit or getattr(sys, "tracebacklimit", None)
            if limit < 0:
                limit = 0
        elif limit:
            limit = abs(limit)

        if isinstance(obj, types.FrameType):
            while obj is not None and limit != 0:
                yield obj, (obj.f_lineno, None, None, None)
                obj = obj.f_back

                if limit:
                    limit -= 1
        elif isinstance(obj, types.TracebackType):
            while obj is not None and limit != 0:
                if sys.version_info >= (3, 11) and obj.tb_lasti >= 0:
                    yield obj.tb_frame, next(itertools.islice(obj.tb_frame.f_code.co_positions(), obj.tb_lasti // 2, None))
                else:
                    yield obj.tb_frame, (obj.tb_lineno, None, None, None)

                obj = obj.tb_next

                if limit:
                    limit -= 1


class PrettyTracebackFormatter(DefaultTracebackFormatter):
    """
    A pretty :class:`.TracebackFormatter`.

    Parameters
    ----------
    theme: :class:`dict`
        A theme.

    Attributes
    ----------
    cause_header: :class:`str`
        The message yielded after an exception's cause.
    context_header: :class:`str`
        The message yielded after an exception's context.
    recursion_cutoff: :class:`int`
        The number of the same frame to display before instead
        displaying a recursion message.
    recursion_message_format: :class:`str`
        The format for the message yielded in place of recursive
        frames.
    theme: :class:`dict`
        A theme.
    traceback_header: :class:`str`
        The message yielded before an exception's traceback.
    """

    __slots__ = ("theme",)

    def __init__(self, *, theme=None):
        self.theme = theme or utils.pretty_theme


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
