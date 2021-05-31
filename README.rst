.. raw:: html

    <p align="center">
        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3AAnalyze+event%3Apush">
            <img alt="Analyze Status" src="https://github.com/ShineyDev/pretty/workflows/Analyze/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ABuild+event%3Apush">
            <img alt="Build Status" src="https://github.com/ShineyDev/pretty/workflows/Build/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ACheck+event%3Apush">
            <img alt="Check Status" src="https://github.com/ShineyDev/pretty/workflows/Check/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ALint+event%3Apush">
            <img alt="Lint Status" src="https://github.com/ShineyDev/pretty/workflows/Lint/badge.svg?event=push" />
        </a>
    </p>

----------

.. raw:: html

    <h1 align="center">pretty</h1>
    <p align="center">A Python module for prettier (and far more useful) stack traces.</p>
    <h6 align="center">Copyright 2020-present ShineyDev</h6>
    <h6 align="center">Inspired by Qix' <a href="https://github.com/Qix-/better-exceptions/">better-exceptions</a></h6>


Install
-------

.. code:: shell

    $ pip install --upgrade git+https://github.com/ShineyDev/pretty.git@main


Use
---

If you wish to hook pretty into **all of your future Python sessions**, set the ``PY_PRETTIFY_EXC`` environment variable to ``1``.


.. code:: shell

    $ export PY_PRETTIFY_EXC=1


If you wish to hook pretty into **a single Python session**, call ``pretty.hook()``.


.. code:: python

    >>> import pretty
    >>> pretty.hook()


If you wish to use the formatters directly, they're `documented <https://docs.shiney.dev/pretty>`_ in the ``pretty.formatter`` module.


.. code:: python

    >>> from pretty.formatter import DefaultFormatter
    >>> formatter = DefaultFormatter()
    >>> print("".join(formatter.format_exception(type(e), e, e.__traceback__)))
