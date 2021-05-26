.. raw:: html

    <p align="center">
        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3AAnalyze+event%3Apush">
            <img alt="Analyze Status"
                 src="https://github.com/ShineyDev/pretty/workflows/Analyze/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ABuild+event%3Apush">
            <img alt="Build Status"
                 src="https://github.com/ShineyDev/pretty/workflows/Build/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ACheck+event%3Apush">
            <img alt="Check Status"
                 src="https://github.com/ShineyDev/pretty/workflows/Check/badge.svg?event=push" />
        </a>

        <a href="https://github.com/ShineyDev/pretty/actions?query=workflow%3ALint+event%3Apush">
            <img alt="Lint Status"
                 src="https://github.com/ShineyDev/pretty/workflows/Lint/badge.svg?event=push" />
        </a>
    </p>

----------

.. raw:: html

    <h1 align="center">pretty</h1>
    <p align="center">A Python module for prettier (and far more useful) stack traces.</p>


Heavily inspired by Qix' `better-exceptions <https://github.com/Qix-/better-exceptions/>`_ module.


Installation
------------

.. code-block:: sh

    python3 -m pip install --upgrade git+https://github.com/ShineyDev/pretty.git


Usage
-----

Not unlike ``better-exceptions``, this module can hook into your python sessions via the ``PY_PRETTIFY_EXC`` environment variable.
