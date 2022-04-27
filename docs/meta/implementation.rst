Implementation
==============

This document outlines the implementation of the project.


Details
-------

pretty.traceback
~~~~~~~~~~~~~~~~

.. currentmodule:: pretty.traceback

- The :class:`~pretty.traceback.TracebackFormatter` abstract class moves some :mod:`traceback`
  module implementations around. You can find each implementation in the following mapping.

  ======================================= =========================================================
  :mod:`traceback`                        :class:`~pretty.traceback.TracebackFormatter`
  ======================================= =========================================================
  :func:`traceback.format_exception`      :attr:`TracebackFormatter.format_traceback(type, value, traceback) <TracebackFormatter.format_traceback>`
  :func:`traceback.format_exc`            :attr:`TracebackFormatter.format_traceback(type(sys.exc_info[1]), sys.exc_info[1], sys.exc_info[2]) <TracebackFormatter.format_traceback>`
  no implementation                       :attr:`TracebackFormatter.format_traceback(type(sys.last_value), sys.last_value, sys.last_traceback)  <TracebackFormatter.format_traceback>`
  :func:`traceback.format_exception_only` :attr:`TracebackFormatter.format_exception(type, value) <TracebackFormatter.format_exception>`
  :func:`traceback.format_list`           :attr:`TracebackFormatter.format_stack(stack)  <TracebackFormatter.format_stack>`
  :func:`traceback.format_stack`          :attr:`TracebackFormatter.format_stack( <TracebackFormatter.format_stack>` :attr:`TracebackFormatter.walk_stack(frame) <TracebackFormatter.walk_stack>` :attr:`) <pretty.traceback.TracebackFormatter.format_stack>`
  :func:`traceback.format_tb`             :attr:`TracebackFormatter.format_stack( <TracebackFormatter.format_stack>` :attr:`TracebackFormatter.walk_stack(traceback) <TracebackFormatter.walk_stack>` :attr:`) <pretty.traceback.TracebackFormatter.format_stack>`
  :func:`traceback.print_exception`       :attr:`TracebackFormatter.print_traceback(type, value, traceback) <pretty.traceback.TracebackFormatter.print_traceback>`
  :func:`traceback.print_exc`             :attr:`TracebackFormatter.print_traceback(type(sys.exc_info[1]), sys.exc_info[1], sys.exc_info[2]) <TracebackFormatter.print_traceback>`
  :func:`traceback.print_last`            :attr:`TracebackFormatter.print_traceback(type(sys.last_value), sys.last_value, sys.last_traceback) <TracebackFormatter.print_traceback>`
  no implementation                       :attr:`TracebackFormatter.print_exception(type, value) <TracebackFormatter.print_exception>`
  ``traceback.print_list()``              :attr:`TracebackFormatter.print_stack(stack) <TracebackFormatter.print_stack>`
  :func:`traceback.print_stack`           :attr:`TracebackFormatter.print_stack( <TracebackFormatter.print_stack>` :attr:`TracebackFormatter.walk_stack(frame) <TracebackFormatter.walk_stack>` :attr:`) <pretty.traceback.TracebackFormatter.print_stack>`
  :func:`traceback.print_tb`              :attr:`TracebackFormatter.print_stack( <TracebackFormatter.print_stack>` :attr:`TracebackFormatter.walk_stack(traceback) <TracebackFormatter.walk_stack>` :attr:`) <pretty.traceback.TracebackFormatter.print_stack>`
  :func:`traceback.walk_stack`            :attr:`TracebackFormatter.walk_stack(frame) <TracebackFormatter.walk_stack>`
  :func:`traceback.walk_tb`               :attr:`TracebackFormatter.walk_stack(traceback) <TracebackFormatter.walk_stack>`
  ======================================= =========================================================
