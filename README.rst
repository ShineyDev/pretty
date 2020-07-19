prettify.py
===========

For prettier (and helpful) Python exceptions.

Heavily inspired by Qix' `better-exceptions <https://github.com/Qix-/better-exceptions/>`_ module. (`LICENSE <https://github.com/ShineyDev/prettify.py/blob/master/LICENSE_QIX/>`_)


Features
--------

#. Everything from ``better-exceptions``, plus;
#. Support for recent Python versions,
#. Slightly more complex debugging,
#. Highly customizable object interface, and;
#. I rewrote the ``traceback.py`` module to get here. :')


Hooking prettify.py
-------------------

Not unlike ``better-exceptions``, this module can hook into your python sessions via the ``PY_PRETTIFY_EXC`` environment variable.
