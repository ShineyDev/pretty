Glossary
========

.. glossary::

    PYTHONPRETTY

        This environment variable can toggle
        :term:`on or off <boolean value>` the
        :term:`main hook <pretty_hook.pth>` for pretty.

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
        :term:`theme <theme value>` by which a :term:`formatter` might
        format its output.

        When this environment variable is set, its value will merge
        with the default pretty theme via
        ``default.update(custom)``.

        When this environment variable is unset, only the default
        pretty theme is used.

    PYTHONPRETTYTRACEBACK

        This environment variable can toggle
        :term:`on or off <boolean value>` the
        :func:`~pretty.traceback.hook` for pretty.traceback.

        When this environment variable is unset,
        :func:`~pretty.traceback.hook` is not called.

        .. important::

            This environment variable is ignored when the
            :term:`PYTHONPRETTY` environment variable is set to a
            :term:`falsey value <boolean value>`.

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

        .. important::

            If the value of a boolean environment variable does not
            match any of the above values, it will fall back to its
            unset behavior.

    theme value

        An environment variable with this value type will correspond to
        a theme dictionary.

        .. TODO

    pretty_hook.pth

        This hook file is installed into site-packages when you install
        pretty. It allows pretty to hook into all Python sessions, but
        will only do so if you set one or more of the above environment
        variables to a :term:`truthy value <boolean value>`.
