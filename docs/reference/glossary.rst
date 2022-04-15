Glossary
========

.. glossary::

    PYTHONPRETTY

        This environment variable can toggle :term:`on or off <boolean value>` the
        :term:`main hook <pretty_hook.pth>` for pretty.

        When this environment variable is set to a :term:`truthy value <boolean value>`, all pretty
        modules will be hooked, unless the module is explicitly disabled with its respective
        :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment variable.

        When this environment variable is set to a :term:`falsey value <boolean value>`, no pretty
        module will be hooked, regardless of the value in its respective
        :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment variable.

        When this environment variable is unset, only the :term:`state <boolean value>` of each
        :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment variable is used.

    PYTHONPRETTYTHEME

        This environment variable can contain a :term:`theme <json value>` by which a formatter
        might format format its output.

        When this environment variable is set, its value will merge with the default pretty theme
        via ``default.update(custom)``.

        When this environment variable is unset, only the default pretty theme is used.

		You can find the meanings of the theme keys in the following mapping.

		.. TODO

    PYTHONPRETTYTRACEBACK

        This environment variable can toggle :term:`on or off <boolean value>` the
        :func:`~pretty.traceback.hook` for pretty.traceback.

        When this environment variable is unset, or the :term:`PYTHONPRETTY` environment variable
        is set to a :term:`falsey value <boolean value>`, :func:`pretty.traceback.hook` is not
        called.

    boolean value

        An environment variable with this value type corresponds to either the boolean value FALSE
        or the boolean value TRUE.

        The following case-insensitive values are considered FALSE:

        - ``0``
        - ``false``
        - ``off``
        - ``disable``
        - ``no``
        - ``n``

        The following case-insensitive values are considered TRUE:

        - ``1``
        - ``true``
        - ``on``
        - ``enable``
        - ``yes``
        - ``y``

        When the value of a boolean environment variable does not match any of the above
        values, it will fall back to its unset behavior.

    json value

        An environment variable with this value type corresponds to a JSON-encoded key-value
        mapping.

    pretty_hook.pth

        A hook file is installed into site-packages when you install pretty. It allows pretty to
        hook into all Python sessions, but will only do so if you set one or more of the above
        :term:`environment variables <PYTHONPRETTY>` to a :term:`truthy value <boolean value>`.
