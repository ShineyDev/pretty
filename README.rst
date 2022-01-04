.. raw:: html

    <p align="center">
        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3AAnalyze">
            <img alt="Analyze Status" src="https://github.com/ShineyDev/pretty/workflows/Analyze/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ABuild">
            <img alt="Build Status" src="https://github.com/ShineyDev/pretty/workflows/Build/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ACheck">
            <img alt="Check Status" src="https://github.com/ShineyDev/pretty/workflows/Check/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ADeploy">
            <img alt="Deploy Status" src="https://github.com/ShineyDev/pretty/workflows/Deploy/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ALint">
            <img alt="Lint Status" src="https://github.com/ShineyDev/pretty/workflows/Lint/badge.svg?event=push" />
        </a>
    </p>

----------

.. raw:: html

    <h1 align="center">ShineyDev/pretty</h1>
    <p align="center">A Python module for prettier (and far more useful) stack traces.<br><a href="https://github.com/ShineyDev/pretty">source</a> | <a href="https://docs.shiney.dev/pretty">documentation</a></p>


Install
-------

.. code:: shell

    $ pip install --upgrade git+https://github.com/ShineyDev/pretty.git@main


Use
---

If you wish to hook pretty.traceback into **all Python sessions**, set the `PYTHONPRETTYTRACEBACK <https://docs.shiney.dev/pretty/latest/environment#term-PYTHONPRETTYTRACEBACK>`_ environment variable to a `truthy value <https://docs.shiney.dev/pretty/latest/environment#term-boolean-value>`_.

.. code:: shell

    $ export PYTHONPRETTYTRACEBACK=1

If you wish to hook pretty.traceback into **a single Python session**, call `pretty.traceback.hook() <https://docs.shiney.dev/pretty/latest/traceback/hook>`_.

.. code:: python

    >>> import pretty
    >>> pretty.traceback.hook()

If you wish to use a formatter directly, initialize a new `PrettyTracebackFormatter <https://docs.shiney.dev/pretty/latest/traceback/pretty>`_ or `DefaultTracebackFormatter <https://docs.shiney.dev/pretty/latest/traceback/default>`_, or build your own implementation on `TracebackFormatter <https://docs.shiney.dev/pretty/latest/traceback/generic>`_.

.. code:: python

    >>> import pretty
    >>>
    >>> formatter = pretty.traceback.PrettyTracebackFormatter()
    >>>
    >>> try:
    >>>     1 / 0
    >>> except Exception as e:
    >>>     print("".join(formatter.format_exception(type(e), e, e.__traceback__)))


.. raw:: html

    <h6 align="center">Copyright 2020-present ShineyDev<br>Inspired by <a href="https://github.com/Qix-/better-exceptions/">Qix-/better-exceptions</a>.</h6>
