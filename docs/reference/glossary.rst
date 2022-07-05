Glossary
========

.. glossary::

    NO_COLOR

        This environment variable can toggle :term:`on or off <boolean value>` ANSI output for all
        `supporting software <https://no-color.org>`_.

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

    SGR value

        A theme item with this value type corresponds to a tuple of two |sgr| values, a single
        |sgr| value, or ``None``.

        When a theme item with this value type is set to ``None``, the corresponding theme item
        will be ignored.

        When a theme items with this value type is set to a tuple of two SGR values, for example
        ``("38;2;255;179;255", "39")``, the values are used as the start and end format for the
        corresponding token.

        When a theme item with this value type is set to a single SGR value, for example ``"1"``,
        the value is used as the start format for the corresponding token, with the end defaulting
        to ``"0"`` (reset).
