Glossary
========

.. glossary::

    PYTHONPRETTY

        This environment variable can toggle
        :term:`on or off <boolean value>` the
        :term:`main hook <pretty_hook.pth>` for pretty.

        .. tip::

            When this environment variable is set to a
            :term:`truthy value <boolean value>`, all pretty modules
            will be hooked, unless the module is explicitly disabled
            with its respective
            :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment
            variable.

            When this environment variable is set to a
            :term:`falsey value <boolean value>`, no pretty module
            will be hooked, regardless of the value in its respective
            :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment
            variable.

            When this environment variable is unset, only the
            :term:`state <boolean value>` of each
            :term:`PYTHONPRETTY... <PYTHONPRETTYTRACEBACK>` environment
            variable is used.

    PYTHONPRETTYTHEME

        This environment variable can contain a
        :term:`theme <theme value>` by which a
        :class:`~pretty.traceback.TracebackFormatter` might format its
        output.

    PYTHONPRETTYTRACEBACK

        This environment variable can toggle
        :term:`on or off <boolean value>` the
        :func:`~pretty.traceback.hook` for pretty.traceback.

    boolean value

        An environment variable with this value type will correspond to
        either the boolean value TRUE or the boolean value FALSE.

        The following case-insensitive values are considered TRUE:

        - ``1``
        - ``true``
        - ``on``
        - ``enable``
        - ``yes``
        - ``y``

        The following case-insensitive values are considered FALSE:

        - ``0``
        - ``false``
        - ``off``
        - ``disable``
        - ``no``
        - ``n``

    theme value

        An environment variable with this value type will correspond to
        a theme dictionary.

        .. TODO

    pretty_hook.pth

        This hook file is installed into site-packages when you install
        pretty. It allows pretty to hook into all Python sessions, but
        will only do so if you set one or more of the above environment
        variables to a :term:`truthy value <boolean value>`.
