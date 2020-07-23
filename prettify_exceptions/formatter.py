"""
/prettify_exceptions/formatter.py

    Copyright (c) 2020 ShineyDev

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import ast
import collections
import inspect
import itertools
import keyword
import linecache
import os
import re
import sys
import traceback
import types


_re_comment = re.compile("((?:(?:\"(?:[^\\\"]|(?:\\\\)*\\\")*\")|(?:\'(?:[^\\\']|(?:\\\\)*\\\')*\')|[^#])*)(#.*)?$")

is_keyword = lambda s: s in keyword.kwlist
is_special_name = lambda s: s.startswith("<") and s.endswith(">")


class _Formatter():
    _default_theme = {
        "cap_char": "\u2514",
        "pipe_char": "\u2502",

        "_ansi_enabled": not os.environ.get("NO_COLOR", False),
        "_bold": "\x1B[1m{0}\x1B[m",
        "comment": "\x1B[38;2;81;163;69m{0}\x1B[m",
        "inspect": "\x1B[38;2;244;144;208m{0}\x1B[m",
        "keyword": "\x1B[38;2;82;153;206m{0}\x1B[m",
        "literal_bool": "\x1B[38;2;82;153;206m{0}\x1B[m",
        "literal_int": "\x1B[38;2;176;203;152m{0}\x1B[m",
        "literal_none": "\x1B[38;2;82;153;206m{0}\x1B[m",
        "literal_str": "\x1B[38;2;208;154;132m{0}\x1B[m",
    }

    _cause_message = traceback._cause_message
    _context_message = traceback._context_message
    _recursive_cutoff = traceback._RECURSIVE_CUTOFF
    _traceback_message = "Traceback (most recent call last):\n"
    _traceback_frame_line_fmt = "    {line}\n"
    _traceback_frame_location_fmt = "  File '{filename}', line {lineno}, in {name}\n"
    _traceback_frame_recursion_fmt = "  [Previous line repeated {count} more time{s}]\n"
    _traceback_frame_scope_fmt = "    {name} = {value}\n"

    class _sentinel: pass

    def __init__(self, **kwargs):
        self.theme = self._default_theme
        self.theme.update(kwargs.get("theme", dict()))

class TracebackFormatter(_Formatter):
    """
    A formatter with reimplementations of the :mod:`traceback` module.
    """

    def extract(self, iterator, *, limit=None, capture_globals=None, capture_locals=None, lookup_lines=None):
        """
        Essentially :meth:`traceback.StackSummary.extract`.
        """

        if capture_globals is None:
            capture_globals = False
        if capture_locals is None:
            capture_locals = False
        if lookup_lines is None:
            lookup_lines = True

        limit = limit or getattr(sys, "tracebacklimit", None)
        if limit is not None:
            if limit >= 0:
                iterator = itertools.islice(iterator, limit)
            else:
                iterator = collections.deque(iterator, -limit)

        result = traceback.StackSummary()
        filenames = set()

        for (frame, lineno) in iterator:
            filename = frame.f_code.co_filename
            filenames.add(filename)
            linecache.lazycache(filename, frame.f_globals)

            name = frame.f_code.co_name
            locals = capture_locals and frame.f_locals or None
            globals = capture_globals and frame.f_globals or None

            result.append(FrameSummary(
                filename, lineno, name, lookup_line=False,
                f_code=frame.f_code, locals=locals, globals=globals))

        for (filename) in filenames:
            linecache.checkcache(filename)

        if lookup_lines:
            for (frame) in result:
                frame.line

        return result

    def extract_stack(self, frame, *, limit=None, capture_globals=None, capture_locals=None, lookup_lines=None):
        """
        Essentially :func:`traceback.extract_stack`.
        """

        return self.extract(
            traceback.walk_stack(frame), limit=limit,
            capture_globals=capture_globals,
            capture_locals=capture_locals, lookup_lines=lookup_lines)

    def extract_traceback(self, exc_traceback, *, limit=None, capture_globals=None, capture_locals=None, lookup_lines=None):
        """
        Essentially :func:`traceback.extract_traceback`.
        """

        return self.extract(
            traceback.walk_tb(exc_traceback), limit=limit,
            capture_globals=capture_globals,
            capture_locals=capture_locals, lookup_lines=lookup_lines)

    def format_exc(self, *, limit=None, chain=True):
        """
        Essentially :func:`traceback.format_exc`.
        """

        yield from self.format_exception(
            *sys.exc_info(), limit=limit, chain=chain)

    def format_exception(self, exc_type, exc_value, exc_traceback, *, limit=None, chain=True, seen=None):
        """
        Essentially :func:`traceback.format_exception`.
        """

        seen = seen or set()
        seen.add(id(exc_value))

        if chain:
            cause = exc_value.__cause__
            context = exc_value.__context__

            if cause is not None and id(cause) not in seen:
                yield from self.format_exception(
                    type(cause), cause, cause.__traceback__,
                    limit=limit, chain=chain, seen=seen)

                yield self._cause_message

            if context is not None and id(context) not in seen:
                yield from self.format_exception(
                    type(context), context, context.__traceback__,
                    limit=limit, chain=chain, seen=seen)

                yield self._context_message

        if exc_traceback is not None:
            yield self._traceback_message

        yield from self.format_traceback(exc_traceback, limit=limit)
        yield from self.format_exception_only(exc_type, exc_value)

    def format_exception_only(self, exc_type, exc_value):
        """
        Alias to :func:`traceback.format_exception_only`.
        """

        yield from traceback.format_exception_only(exc_type, exc_value)

    def format_list(self, list_):
        """
        Essentially :func:`traceback.format_list`.
        """

        count = 0
        last_filename = None
        last_lineno = None
        last_name = None

        for (frame) in list_:
            filename, lineno, name, line = frame
            if not isinstance(frame, traceback.FrameSummary):
                frame = None

            if (last_filename is None or last_filename != filename or
                last_lineno is None or last_lineno != lineno or
                last_name is None or last_name != name):
                if count > self._recursive_cutoff:
                    count -= self._recursive_cutoff
                    yield self._traceback_frame_recursion_fmt.format(
                        count=count,
                        s=count != 1 and "s" or "")

                count = 0
                last_filename, last_lineno, last_name = \
                    filename, lineno, name

            count += 1
            if count > self._recursive_cutoff:
                continue

            yield from self.format_list_frame(
                frame, filename, lineno, name, line)

        if count > self._recursive_cutoff:
            count -= self._recursive_cutoff
            yield self._traceback_frame_recursion_fmt.format(
                count=count,
                s=count != 1 and "s" or "")

    def format_list_frame(self, frame, filename, lineno, name, line):
        """
        Essentially :meth:`traceback.StackSummary.format`'s ``row`` logic.
        """

        yield self._traceback_frame_location_fmt.format(
            filename=filename, lineno=lineno, name=name)

        if line:
            yield self._traceback_frame_line_fmt.format(line=line)

        if frame and frame.locals:
            for (name, value) in sorted(frame.locals.items()):
                yield self._traceback_frame_scope_fmt.format(
                    name=name, value=repr(value))

    def format_stack(self, frame, *, limit=None, capture_globals=None, capture_locals=None, lookup_lines=None):
        """
        Essentially :func:`traceback.format_stack`.
        """

        yield from self.format_list(self.extract_stack(
            frame, limit=limit, capture_globals=capture_globals,
            capture_locals=capture_locals, lookup_lines=lookup_lines))

    def format_traceback(self, exc_traceback, *, limit=None, capture_globals=None, capture_locals=None, lookup_lines=None):
        """
        Essentially :func:`traceback.format_traceback`.
        """

        yield from self.format_list(self.extract_traceback(
            exc_traceback, limit=limit, capture_globals=capture_globals,
            capture_locals=capture_locals, lookup_lines=lookup_lines))

class DefaultFormatter(TracebackFormatter):
    _recursive_cutoff = 1
    _traceback_frame_recursion_fmt = "  [Previous frame repeated {count} more time{s}]\n\n"

    def format_list_frame(self, frame, filename, lineno, name, line):
        if not line:
            line = linecache.getline(filename, lineno, frame.globals)

        if frame and not is_special_name(name):
            fmt = self._traceback_frame_location_fmt[:-1]
            fmt += "{signature}\n"

            try:
                signature = inspect.signature(
                    types.FunctionType(frame.f_code, {}))
            except (TypeError) as e:
                # TODO: handle closures
                signature = "(<unknown>)"

            yield self.colorize(fmt.format(
                filename=filename, lineno=lineno, name=name,
                signature=signature), "_bold")
        else:
            yield self.colorize(self._traceback_frame_location_fmt.format(
                filename=filename, lineno=lineno, name=name), "_bold")

        if not line:
            # still don't have a line?
            # probably in a repl;
            # let's not expand the trace.
            return

        try:
            tree = ast.parse(line, filename, "exec")
        except (SyntaxError) as e:
            yield self._traceback_frame_line_fmt.format(line=line)
            yield "\n"
            return
        
        if self.theme["_ansi_enabled"]:
            line = self.colorize_tree(tree, line)

        yield self._traceback_frame_line_fmt.format(line=line)

        if frame:
            yield from self.inspect(tree, frame)

    def format_traceback(self, exc_traceback, *, limit=None, lookup_lines=True):
        return super().format_traceback(
            exc_traceback, limit=limit, capture_globals=True,
            capture_locals=True, lookup_lines=lookup_lines)

    def colorize(self, source, theme):
        if theme and self.theme["_ansi_enabled"]:
            return self.theme[theme].format(source)

        return source

    def colorize_tree(self, tree, line):
        colorize = []
        
        for (node) in ast.walk(tree):
            if not hasattr(node, "col_offset") or not hasattr(node, "end_col_offset"):
                continue

            cls = node.__class__
            name = cls.__name__
            source = line[node.col_offset:node.end_col_offset]

            col_offset = node.col_offset

            if cls is ast.Constant:
                theme = self._get_theme(node.value)
                colorize.append((col_offset, source, theme))

        colorize.sort(key=lambda e: e[0])
        
        chunks = []
        offset = 0

        for (col_offset, source, theme) in colorize:
            chunks.append(line[offset:col_offset])
            chunks.append(self.colorize(source, theme))
            offset = col_offset + len(source)

        chunks.append(line[offset:])

        line = "".join(chunks)

        match = _re_comment.fullmatch(line)
        if match and match.group(2):
            line = "{0}{1}".format(
                match.group(1),
                self.colorize(match.group(2), "comment"))

        return line

    def colorize_value(self, value):
        value_repr = repr(value)

        theme = self._get_theme(value)
        if theme:
            value_repr = self.colorize(value_repr, theme)

        return value_repr

    def get_relevant_values(self, tree, frame):
        values = []

        for (node) in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                if not isinstance(node.value, ast.Name):
                    continue

                value = frame.scope.get(node.value.id, self._sentinel)

                if value is not self._sentinel:
                    value = getattr(value, node.attr, self._sentinel)

                if value is not self._sentinel:
                    values.append((node.col_offset + len(node.value.id) + 1, value))

            if isinstance(node, ast.Name):
                value = frame.scope.get(node.id, self._sentinel)

                if value is not self._sentinel:
                    values.append((node.col_offset, value))

        values.sort(key=lambda e: e[0])

        return values

    def inspect(self, tree, frame):
        values = self.get_relevant_values(tree, frame)
        values = [(o, v, self.colorize_value(v)) for (o, v) in values]
        while values:
            col_offset, value, value_repr = values.pop()

            this_line = list()
            this_line.append((col_offset, value, value_repr))

            index = col_offset
            for (i) in reversed(range(len(values))):
                col_offset, value, value_repr = values[i]

                if col_offset + len(repr(value)) + 2 < index:
                    values.pop(i)
                    this_line.append((col_offset, value, value_repr))
                    index = col_offset
                else:
                    this_line.append((col_offset, None, None))
                    index = col_offset

            this_line.sort(key=lambda e: e[0])

            index = 0
            line = ""

            for (col_offset, value, value_repr) in this_line:
                line += " " * (col_offset - index)

                if value_repr is None:
                    line += self.colorize(
                        self.theme["pipe_char"], "inspect")

                    index = col_offset + 1

                    continue

                line += "{0} {1}".format(
                    self.colorize(self.theme["cap_char"], "inspect"),
                    self.colorize(value_repr, "inspect"))

                index = col_offset + len(repr(value)) + 2

            yield self._traceback_frame_line_fmt.format(line=line)

        yield "\n"

    def _get_theme(self, value):
        theme = None

        if isinstance(value, bool):
            theme = "literal_bool"
        elif isinstance(value, (complex, float, int)):
            theme = "literal_int"
        elif isinstance(value, type(None)):
            theme = "literal_none"
        elif isinstance(value, (bytes, str)):
            theme = "literal_str"

        return theme

class FrameSummary(traceback.FrameSummary):
    __slots__ = ("filename", "lineno", "name", "_line", "f_code", "locals", "globals", "scope")

    def __init__(self, filename, lineno, name, *, lookup_line=True, line=None, f_code=None, locals=None, globals=None):
        super().__init__(filename, lineno, name, lookup_line=lookup_line, locals=None, line=line)

        self.f_code = f_code
        self.locals = locals or dict()
        self.globals = globals or dict()

        self.scope = self.globals.copy()
        self.scope.update(self.locals)
