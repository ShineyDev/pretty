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

        The theme can contain the following keys.

        .. describe:: ast_comment_sgr

            The :term:`SGR value` given to |token_comment|.

        .. describe:: ast_delimiter_sgr

            The :term:`SGR value` given to the following |token_delimiter|.

            - ``(``
            - ``)``
            - ``[``
            - ``]``
            - ``{``
            - ``}``
            - ``,``
            - ``:``
            - ``.``
            - ``;``
            - ``\``

        .. describe:: ast_keyword_sgr
        
            The :term:`SGR value` given to the following |token_keyword|.

            - ``_`` (in Python 3.10+ as described by |token_soft_keyword|)
            - ``and``
            - ``as``
            - ``assert``
            - ``async``
            - ``await``
            - ``break``
            - ``case`` (in Python 3.10+ as described by |token_soft_keyword|)
            - ``class``
            - ``continue``
            - ``def``
            - ``del``
            - ``elif``
            - ``else``
            - ``except``
            - ``finally``
            - ``for``
            - ``from``
            - ``global``
            - ``if``
            - ``import``
            - ``in``
            - ``is``
            - ``lambda``
            - ``match`` (in Python 3.10+ as described by |token_soft_keyword|)
            - ``nonlocal``
            - ``not``
            - ``or``
            - ``pass``
            - ``raise``
            - ``return``
            - ``try``
            - ``while``
            - ``with``
            - ``yield``

        .. describe:: ast_name_sgr

            The :term:`SGR value` given to |token_name| that do not fall under another ``ast_*`` or
            ``literal_*``.

        .. describe:: ast_operator_sgr

            The :term:`SGR value` given to |token_operator|.

    PYTHONPRETTYTRACEBACK

        This environment variable can toggle :term:`on or off <boolean value>` the
        :func:`~pretty.traceback.hook` for pretty.traceback.

        When this environment variable is set to a :term:`truthy value <boolean value>`, and the
        :term:`PYTHONPRETTY` environment variable set to a :term:`truthy value <boolean value>` or
        unset, :func:`pretty.traceback.hook` is called.

        When this environment variable is set to a :term:`falsey value <boolean value>`, unset, or
        the :term:`PYTHONPRETTY` environment variable is set to a
        :term:`falsey value <boolean value>`, :func:`pretty.traceback.hook` is not called.

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
