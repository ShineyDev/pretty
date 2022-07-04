Environment
===========

.. glossary::

    PYTHONPRETTY

        This environment variable can toggle :term:`on or off <boolean value>` the
        :term:`main hook <pretty_hook.pth>` for pretty.

        When this environment variable is set to a :term:`truthy value <boolean value>` all pretty
        modules will be hooked, unless the module is explicitly disabled with its respective
        :term:`PYTHONPRETTY* <PYTHONPRETTYTRACEBACK>` environment variable.

        This means that in order to enable, say, all pretty modules bar pretty.traceback you could
        set :term:`PYTHONPRETTY` to a :term:`truthy value <boolean value>` and set
        :term:`PYTHONPRETTYTRACEBACK` to a :term:`falsey value <boolean value>`.

        When this environment variable is set to a :term:`falsey value <boolean value>` no pretty
        module will be hooked, regardless of the :term:`state <boolean value>` of its respective
        :term:`PYTHONPRETTY* <PYTHONPRETTYTRACEBACK>` environment variable.

        This means that in order to temporarily disable pretty output, you can simply set
        :term:`PYTHONPRETTY` to a :term:`falsey value <boolean value>`.

        When this environment variable is unset, the :term:`state <boolean value>` of each
        :term:`PYTHONPRETTY* <PYTHONPRETTYTRACEBACK>` environment variable is used to determine
        whether its respective module will be hooked.

.. glossary::

    PYTHONPRETTYANSI

        This environment variable can toggle :term:`on or off <boolean value>` ANSI output for
        pretty.

        When this environment variable is set to a :term:`truthy value <boolean value>` ANSI output
        will be enabled, regardless of the state of the :term:`NO_COLOR` environment variable.

        When this environment variable is set to a :term:`falsey value <boolean value>` ANSI output
        will be disabled, regardless of the state of the :term:`NO_COLOR` environment variable.

        When this environment variable is unset the value of the :term:`NO_COLOR` environment
        variable is considered, before ANSI output remains enabled by default.
