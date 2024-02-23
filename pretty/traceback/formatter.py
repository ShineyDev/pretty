from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from typing import Any, TextIO, cast, overload
    from typing_extensions import Self

    from traceback import FrameSummary, StackSummary
    from types import FrameType, TracebackType

import abc
import itertools
import linecache
import sys
import textwrap
import traceback
import types

import pretty
from pretty.utility import MISSING


class TracebackFormatter(metaclass=abc.ABCMeta):
    """
    An abstract class for building a traceback formatter.
    """

    __slots__ = ()

    @abc.abstractmethod
    def format_exception(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        /,
    ) -> Iterator[str]:
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
    def format_frame(
        self: Self,
        frame: tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]],
        /,
        *,
        display_locals: bool = MISSING,
    ) -> Iterator[str]:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_stack(
        self: Self,
        stack: Iterable[tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]]],
        /,
        *,
        display_locals: bool = MISSING,
    ) -> Iterator[str]:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    @abc.abstractmethod
    def format_traceback(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        traceback: TracebackType | None,
        /,
        *,
        chain: bool = MISSING,
        display_locals: bool = MISSING,
        limit: int = MISSING,
    ) -> Iterator[str]:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        limit: :class:`int`
            The maximum number of frames to extract.


        :yields: :class:`str`
        """

        raise NotImplementedError

        yield

    def print_exception(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        /,
        *,
        stream: TextIO = MISSING,
    ) -> None:
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

    def print_frame(
        self: Self,
        frame: tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]],
        /,
        *,
        display_locals: bool = MISSING,
        stream: TextIO = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_frame(frame, display_locals=display_locals, stream=stream or sys.stderr)

    def print_stack(
        self: Self,
        stack: Iterable[tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]]],
        /,
        *,
        display_locals: bool = MISSING,
        stream: TextIO = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_stack(stack, display_locals=display_locals, stream=stream or sys.stderr)

    def print_traceback(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        traceback: TracebackType | None,
        /,
        *,
        chain: bool = MISSING,
        display_locals: bool = MISSING,
        limit: int = MISSING,
        stream: TextIO = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        limit: :class:`int`
            The maximum number of frames to extract.
        stream: :func:`TextIO <open>`
            The stream to print to. Defaults to :data:`~sys.stderr`.
        """

        self.write_traceback(type, value, traceback, chain=chain, display_locals=display_locals, limit=limit, stream=stream or sys.stderr)

    @abc.abstractmethod
    def walk_stack(
        self: Self,
        obj: FrameType | TracebackType,
        /,
        *,
        limit: int = MISSING,
    ) -> Iterator[tuple[FrameType, tuple[int, int | None, int | None, int | None]]]:
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

    def write_exception(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        /,
        *,
        stream: TextIO,
    ) -> None:
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

    def write_frame(
        self: Self,
        frame: tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]],
        /,
        *,
        stream: TextIO,
        display_locals: bool = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        """

        stream.write("".join(self.format_frame(frame, display_locals=display_locals)))

    def write_stack(
        self: Self,
        stack: Iterable[tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]]],
        /,
        *,
        stream: TextIO,
        display_locals: bool = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        """

        stream.write("".join(self.format_stack(stack, display_locals=display_locals)))

    def write_traceback(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        traceback: TracebackType | None,
        /,
        *,
        stream: TextIO,
        chain: bool = MISSING,
        display_locals: bool = MISSING,
        limit: int = MISSING,
    ) -> None:
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
        display_locals: Optional[:class:`bool`]
            Whether to display the locals in each frame. Defaults to
            ``None`` when no value is given, but expects a boolean.
        limit: :class:`int`
            The maximum number of frames to extract.
        """

        stream.write("".join(self.format_traceback(type, value, traceback, chain=chain, display_locals=display_locals, limit=limit)))

    @pretty.utility.wrap_fallback(traceback.extract_stack)  # type: ignore  # it doesn't like self
    def _extract_stack(
        self: Self,
        f: FrameType | None = None,
        limit: int | None = None,
    ) -> StackSummary:
        frame = f or sys._getframe().f_back

        if TYPE_CHECKING:
            frame = cast(FrameType, frame)

        options: dict[str, Any] = dict()

        if limit is not None:
            options["limit"] = limit

        generator = self.walk_stack(frame, **options)

        if sys.version_info >= (3, 11):
            extract = traceback.StackSummary._extract_from_extended_frame_gen  # type: ignore  # StackSummary._extract_from_extended_frame_gen does exist
        else:
            extract = traceback.StackSummary.extract

            def generator_function():
                for frame, position in generator:
                    yield frame, position[0]

            generator = generator_function()

        stack = extract(generator)
        stack.reverse()

        return stack

    @pretty.utility.wrap_fallback(traceback.extract_tb)  # type: ignore  # it doesn't like self
    def _extract_tb(
        self: Self,
        tb: TracebackType | None = None,
        limit: int | None = None,
    ) -> StackSummary:
        if not tb:
            return traceback.StackSummary()

        options: dict[str, Any] = dict()

        if limit is not None:
            options["limit"] = limit

        generator = self.walk_stack(tb, **options)

        if sys.version_info >= (3, 11):
            extract = traceback.StackSummary._extract_from_extended_frame_gen  # type: ignore  # StackSummary._extract_from_extended_frame_gen does exist
        else:
            extract = traceback.StackSummary.extract

            def generator_function():
                for frame, position in generator:
                    yield frame, position[0]

            generator = generator_function()

        stack = extract(generator)

        return stack

    @pretty.utility.wrap_fallback(traceback.format_exc)  # type: ignore  # it doesn't like self
    def _format_exc(
        self: Self,
        limit: int | None = None,
        chain: bool = True,
    ) -> str:
        _, value, traceback = sys.exc_info()

        options: dict[str, Any] = {
            "chain": chain,
        }

        if limit is not None:
            options["limit"] = limit

        return "".join(self.format_traceback(value.__class__, value, traceback, chain=chain, **options))

    if sys.version_info >= (3, 10):

        if TYPE_CHECKING:

            @overload
            def _format_exception(
                self: Self,
                exc: BaseException,
                /,
                *,
                limit: int | None = ...,
                chain: bool = ...,
            ) -> list[str]: ...

            @overload
            def _format_exception(
                self: Self,
                exc: type[BaseException] | None,
                /,
                value: BaseException | None,
                tb: TracebackType | None,
                limit: int | None = ...,
                chain: bool = ...,
            ) -> list[str]: ...

        @pretty.utility.wrap_fallback(traceback.format_exception)  # type: ignore  # it doesn't like self
        def _format_exception(
            self: Self,
            exc: BaseException | type[BaseException] | None,
            /,
            value: BaseException | None = traceback._sentinel,  # type: ignore  # traceback._sentinel does exist
            tb: TracebackType | None = traceback._sentinel,  # type: ignore  # traceback._sentinel does exist
            limit: int | None = None,
            chain: bool = True,
        ) -> list[str]:
            if (value is traceback._sentinel) != (tb is traceback._sentinel):  # type: ignore  # traceback._sentinel does exist
                raise ValueError("Both or neither of value and tb must be given")
            elif value is traceback._sentinel:  # type: ignore  # traceback._sentinel does exist
                if exc is None:
                    value, tb = None, None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {type(exc).__name__} found")

                    value, tb = exc, exc.__traceback__  # type: ignore  # this isn't my problem

            options: dict[str, Any] = {
                "chain": chain,
            }

            if limit is not None:
                options["limit"] = limit

            return list(self.format_traceback(value.__class__, value, tb, **options))

        if TYPE_CHECKING:

            @overload
            def _format_exception_only(
                self: Self,
                exc: BaseException,
                /,
            ) -> list[str]: ...

            @overload
            def _format_exception_only(
                self: Self,
                exc: type[BaseException] | None,
                /,
                value: BaseException | None,
            ) -> list[str]: ...

        @pretty.utility.wrap_fallback(traceback.format_exception_only)  # type: ignore  # it doesn't like self
        def _format_exception_only(
            self: Self,
            exc: BaseException | type[BaseException] | None,
            /,
            value: BaseException | None = traceback._sentinel,  # type: ignore  # traceback._sentinel does exist
        ) -> list[str]:
            if value is traceback._sentinel:  # type: ignore  # traceback._sentinel does exist
                if exc is None:
                    value = None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {type(exc).__name__} found")

                    value = exc  # type: ignore  # this isn't my problem

            return list(self.format_exception(value.__class__, value))

    else:

        @pretty.utility.wrap_fallback(traceback.format_exception)  # type: ignore  # it doesn't like self
        def _format_exception(
            self: Self,
            etype: type[BaseException] | None,
            value: BaseException | None,
            tb: TracebackType | None,
            limit: int | None = None,
            chain: bool = True,
        ) -> list[str]:
            options: dict[str, Any] = {
                "chain": chain,
            }

            if limit is not None:
                options["limit"] = limit

            return list(self.format_traceback(value.__class__, value, tb, **options))

        @pretty.utility.wrap_fallback(traceback.format_exception_only)  # type: ignore  # it doesn't like self
        def _format_exception_only(
            self: Self,
            etype: type[BaseException] | None,
            value: BaseException | None,
        ) -> list[str]:
            return list(self.format_exception(value.__class__, value))

    @pretty.utility.wrap_fallback(traceback.format_list)  # type: ignore  # it doesn't like self
    def _format_list(
        self: Self,
        extracted_list: list[FrameSummary | tuple[str, int, str, str]],
    ) -> list[str]:
        return list(self.format_stack((traceback.FrameSummary(filename, lineno, name, line=line), (lineno, None, None, None)) for (filename, lineno, name, line) in extracted_list))

    @pretty.utility.wrap_fallback(traceback.format_stack)  # type: ignore  # it doesn't like self
    def _format_stack(
        self: Self,
        f: FrameType | None = None,
        limit: int | None = None,
    ) -> list[str]:
        frame = f or sys._getframe().f_back

        if TYPE_CHECKING:
            frame = cast(FrameType, frame)

        options = dict()

        if limit is not None:
            options["limit"] = limit

        return list(self.format_stack(self.walk_stack(frame, **options)))

    @pretty.utility.wrap_fallback(traceback.format_tb)  # type: ignore  # it doesn't like self
    def _format_tb(
        self: Self,
        tb: TracebackType | None,
        limit: int | None = None,
    ) -> list[str]:
        if not tb:
            return list()
        else:
            options = dict()

            if limit is not None:
                options["limit"] = limit

            return list(self.format_stack(self.walk_stack(tb, **options)))

    @pretty.utility.wrap_fallback(traceback.print_exc)  # type: ignore  # it doesn't like self
    def _print_exc(
        self,
        limit: int | None = None,
        file: TextIO | None = None,
        chain: bool = True,
    ) -> None:
        _, value, traceback = sys.exc_info()

        options: dict[str, Any] = {
            "chain": chain,
        }

        if file is not None:
            options["stream"] = file

        if limit is not None:
            options["limit"] = limit

        self.print_traceback(value.__class__, value, traceback, **options)

    if sys.version_info >= (3, 10):

        if TYPE_CHECKING:

            @overload
            def _print_exception(
                self: Self,
                exc: BaseException,
                /,
                *,
                limit: int | None = ...,
                file: TextIO | None = ...,
                chain: bool = ...,
            ) -> None: ...

            @overload
            def _print_exception(
                self: Self,
                exc: type[BaseException] | None,
                /,
                value: BaseException | None,
                tb: TracebackType | None,
                limit: int | None = ...,
                file: TextIO | None = ...,
                chain: bool = ...,
            ) -> None: ...

        @pretty.utility.wrap_fallback(traceback.print_exception)  # type: ignore  # it doesn't like self
        def _print_exception(
            self: Self,
            exc: BaseException | type[BaseException] | None,
            /,
            value: BaseException | None = traceback._sentinel,  # type: ignore  # traceback._sentinel does exist
            tb: TracebackType | None = traceback._sentinel,  # type: ignore  # traceback._sentinel does exist
            limit: int | None = None,
            file: TextIO | None = None,
            chain: bool = True,
        ) -> None:
            if (value is traceback._sentinel) != (tb is traceback._sentinel):  # type: ignore  # traceback._sentinel does exist
                raise ValueError("Both or neither of value and tb must be given")
            elif value is traceback._sentinel:  # type: ignore  # traceback._sentinel does exist
                if exc is None:
                    value, tb = None, None
                else:
                    if sys.version_info >= (3, 11):
                        if not isinstance(exc, BaseException):
                            raise TypeError(f"Exception expected for value, {type(exc).__name__} found")

                    value, tb = exc, exc.__traceback__  # type: ignore  # this isn't my problem

            options: dict[str, Any] = {
                "chain": chain,
            }

            if file is not None:
                options["stream"] = file

            if limit is not None:
                options["limit"] = limit

            self.print_traceback(value.__class__, value, tb, **options)

    else:

        @pretty.utility.wrap_fallback(traceback.print_exception)  # type: ignore  # it doesn't like self
        def _print_exception(
            self: Self,
            etype: type[BaseException] | None,
            value: BaseException | None,
            tb: TracebackType | None,
            limit: int | None = None,
            file: TextIO | None = None,
            chain: bool = True,
        ) -> None:
            options: dict[str, Any] = {
                "chain": chain,
            }

            if file is not None:
                options["stream"] = file

            if limit is not None:
                options["limit"] = limit

            self.print_traceback(value.__class__, value, tb, **options)

    @pretty.utility.wrap_fallback(traceback.print_last)  # type: ignore  # it doesn't like self
    def _print_last(
        self: Self,
        limit: int | None = None,
        file: TextIO | None = None,
        chain: bool = True,
    ) -> None:
        if not hasattr(sys, "last_type"):
            raise ValueError("no last exception")

        value, traceback = sys.last_value, sys.last_traceback

        options: dict[str, Any] = {
            "chain": chain,
        }

        if file is not None:
            options["stream"] = file

        if limit is not None:
            options["limit"] = limit

        self.print_traceback(value.__class__, value, traceback, **options)

    @pretty.utility.wrap_fallback(traceback.print_list)  # type: ignore  # it doesn't like self
    def _print_list(
        self: Self,
        extracted_list: list[FrameSummary | tuple[str, int, str, str]],
        file: TextIO | None = None,
    ) -> None:
        options: dict[str, Any] = dict()

        if file is not None:
            options["stream"] = file

        self.print_stack(((traceback.FrameSummary(filename, lineno, name, line=line), (lineno, None, None, None)) for (filename, lineno, name, line) in extracted_list), **options)

    @pretty.utility.wrap_fallback(traceback.print_stack)  # type: ignore  # it doesn't like self
    def _print_stack(
        self: Self,
        f: FrameType | None = None,
        limit: int | None = None,
        file: TextIO | None = None,
    ) -> None:
        frame = f or sys._getframe().f_back

        if TYPE_CHECKING:
            frame = cast(FrameType, frame)

        walk_options: dict[str, Any] = dict()

        if limit is not None:
            walk_options["limit"] = limit

        print_options: dict[str, Any] = dict()

        if file is not None:
            walk_options["stream"] = file

        self.print_stack(self.walk_stack(frame, **walk_options), **print_options)

    @pretty.utility.wrap_fallback(traceback.print_tb)  # type: ignore  # it doesn't like self
    def _print_tb(
        self: Self,
        tb: TracebackType | None,
        limit: int | None = None,
        file: TextIO | None = None,
    ) -> None:
        if tb:
            walk_options: dict[str, Any] = dict()

            if limit is not None:
                walk_options["limit"] = limit

            print_options: dict[str, Any] = dict()

            if file is not None:
                walk_options["stream"] = file

            self.print_stack(self.walk_stack(tb, **walk_options), **print_options)

    @pretty.utility.wrap_fallback(traceback.walk_stack)  # type: ignore  # it doesn't like self
    def _walk_stack(
        self: Self,
        f: FrameType | None,
    ) -> Iterator[tuple[FrameType, int]]:
        if sys.version_info >= (3, 11):
            frame = f or sys._getframe().f_back.f_back.f_back.f_back  # type: ignore  # frame -4 does exist here when called normally
        else:
            frame = f or sys._getframe().f_back.f_back  # type: ignore  # frame -2 does exist here when called normally

        if TYPE_CHECKING:
            frame = cast(FrameType, frame)

        for frame, position in self.walk_stack(frame):
            yield frame, position[0]

    @pretty.utility.wrap_fallback(traceback.walk_tb)  # type: ignore  # it doesn't like self
    def _walk_tb(
        self: Self,
        tb: TracebackType,
    ) -> Iterator[tuple[FrameType, int]]:
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
    location_format = "File \"{filename}\", line {lineno}, in {name}"  # fmt: skip
    recursion_cutoff = 3
    recursion_message_format = "[Previous line repeated {times} more time{times_s}]"
    traceback_header = "Traceback (most recent call last):"

    def format_exception(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        /,
    ) -> Iterator[str]:
        type_name = pretty.utility.try_name(type, default="<type.__name__ failed>")
        value_str = pretty.utility.try_str(value, default="<value.__str__ failed>")

        if value_str:
            yield f"{type_name}: {value_str}\n"
        else:
            yield f"{type_name}\n"

        if sys.version_info >= (3, 11):
            notes = getattr(value, "__notes__", None)
            if notes:
                for note in notes:
                    note = pretty.utility.try_str(note, default="<note.__str__ failed>")
                    for line in note.splitlines():
                        yield f"{line}\n"

    def format_frame(
        self: Self,
        frame: tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]],
        /,
        *,
        display_locals: bool | None = None,
    ) -> Iterator[str]:
        frame_summary, frame_position = frame

        if TYPE_CHECKING:
            frame_summary: FrameSummary | FrameType
            frame_position: tuple[int, int | None, int | None, int | None]

        if isinstance(frame_summary, types.FrameType):
            filename = frame_summary.f_code.co_filename
            name = frame_summary.f_code.co_name
        else:
            filename = frame_summary.filename
            name = frame_summary.name

        lineno = frame_position[0]

        yield self.location_format.format(filename=filename, lineno=lineno, name=name) + "\n"

        if isinstance(frame_summary, types.FrameType):
            line = linecache.getline(filename, lineno)
        else:
            line = frame_summary.line

        if line:
            yield line

        if display_locals is None:
            display_locals = False

        if display_locals:
            if isinstance(frame_summary, types.FrameType):
                locals = frame_summary.f_locals
            else:
                locals = frame_summary.locals

            if locals:
                for key, value in sorted(locals.items()):
                    if isinstance(frame_summary, types.FrameType):
                        value = pretty.utility.try_repr(value, default="<value.__repr__ failed>")

                    yield f"  {key} = {value}\n"

    def format_stack(
        self: Self,
        stack: Iterable[tuple[FrameSummary | FrameType, tuple[int, int | None, int | None, int | None]]],
        /,
        *,
        display_locals: bool | None = None,
    ) -> Iterator[str]:
        last_filename = None
        last_lineno = None
        last_name = None
        recursion_times = 0

        for frame_summary, frame_position in stack:
            if isinstance(frame_summary, types.FrameType):
                current_filename = frame_summary.f_code.co_filename
                current_name = frame_summary.f_code.co_name
            else:
                current_filename = frame_summary.filename
                current_name = frame_summary.name

            current_lineno = frame_position[0]

            if current_filename != last_filename or current_lineno != last_lineno or current_name != last_name:
                if recursion_times > self.recursion_cutoff:
                    times = recursion_times - self.recursion_cutoff
                    yield self.recursion_message_format.format(times=times, times_s="" if times == 1 else "s") + "\n"

                last_filename = current_filename
                last_lineno = current_lineno
                last_name = current_name
                recursion_times = 0

            recursion_times += 1

            if recursion_times > self.recursion_cutoff:
                continue

            yield from self.format_frame((frame_summary, frame_position), display_locals=display_locals)

        if recursion_times > self.recursion_cutoff:
            times = recursion_times - self.recursion_cutoff
            yield self.recursion_message_format.format(times=times, times_s="" if times == 1 else "s") + "\n"

    def format_traceback(
        self: Self,
        type: type[BaseException] | type[None],
        value: BaseException | None,
        traceback: TracebackType | None,
        /,
        *,
        chain: bool | None = None,
        display_locals: bool | None = None,
        limit: int | None = None,
        seen: set | None = None,
    ) -> Iterator[str]:
        if chain is None:
            chain = True

        if chain and value is not None:
            seen = seen or set()
            seen.add(id(value))

            cause = value.__cause__

            if cause is not None and id(cause) not in seen:
                yield from self.format_traceback(cause.__class__, cause, cause.__traceback__, chain=chain, limit=limit, seen=seen)
                yield f"\n{self.cause_header}\n\n"

            context = value.__context__
            context_suppressed = value.__suppress_context__

            if cause is None and context is not None and not context_suppressed and id(context) not in seen:
                yield from self.format_traceback(context.__class__, context, context.__traceback__, chain=chain, limit=limit, seen=seen)
                yield f"\n{self.context_header}\n\n"

        if traceback is not None:
            yield f"{self.traceback_header}\n"

            for line in self.format_stack(self.walk_stack(traceback, limit=limit), display_locals=display_locals):
                yield textwrap.indent(line, "  ")

        yield from self.format_exception(type, value)

    def walk_stack(
        self: Self,
        obj: FrameType | TracebackType,
        /,
        *,
        limit: int | None = None,
    ) -> Iterator[tuple[FrameType, tuple[int, int | None, int | None, int | None]]]:
        if limit is not None:
            limit = max(limit, 0)
        elif isinstance(obj, types.TracebackType):
            limit = limit or getattr(sys, "tracebacklimit", None)
            if limit and limit < 0:
                limit = 0

        if isinstance(obj, types.FrameType):
            frame = obj

            while frame is not None and limit != 0:
                yield frame, (frame.f_lineno, None, None, None)
                frame = frame.f_back

                if limit:
                    limit -= 1
        elif isinstance(obj, types.TracebackType):
            traceback = obj

            while traceback is not None and limit != 0:
                if sys.version_info >= (3, 11):
                    if traceback.tb_lasti >= 0:
                        yield traceback.tb_frame, next(itertools.islice(traceback.tb_frame.f_code.co_positions(), traceback.tb_lasti // 2, None))
                    else:
                        yield traceback.tb_frame, (traceback.tb_lineno, None, None, None)
                else:
                    yield traceback.tb_frame, (traceback.tb_lineno, None, None, None)

                traceback = traceback.tb_next

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

    def __init__(
        self: Self,
        /,
        *,
        theme: dict[str, Any] | None = None,
    ) -> None:
        self.theme = (theme or pretty.utility.pretty_theme).copy()


__all__ = [
    "TracebackFormatter",
    "DefaultTracebackFormatter",
    "PrettyTracebackFormatter",
]
