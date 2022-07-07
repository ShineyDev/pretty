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

    PYTHONPRETTYTRACEBACK

        This environment variable can toggle :term:`on or off <boolean value>` the
        :func:`~pretty.traceback.hook` for pretty.traceback.

        When this environment variable is set to a :term:`truthy value <boolean value>`, after
        considering the state of the :term:`PYTHONPRETTY` environment variable,
        :func:`pretty.traceback.hook` is called.

        When this environment variable is set to a :term:`falsey value <boolean value>`
        :func:`pretty.traceback.hook` is not called.

        When this environment variable is unset, after considering the state of the
        :term:`PYTHONPRETTY` environment variable, :func:`pretty.traceback.hook` is not called.

.. glossary::

    PYTHONPRETTYTHEME

        This environment variable can contain a :term:`theme <json value>` by which a formatter
        might format its output.

        When this environment variable is set, its value will merge with the default pretty theme
        via ``default.update(custom)``.

        When this environment variable is unset, the default pretty theme is used.

        The theme can contain the following keys.

        .. describe:: ast_comment_sgr

            The :term:`SGR value` given to |token_comment| in an |ast|.

        .. describe:: ast_delimiter_sgr

            The :term:`SGR value` given to the following |token_delimiter| in an |ast|.

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
        
            The :term:`SGR value` given to the following |token_keyword| in an |ast|.

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

            The :term:`SGR value` given to |token_name| in an |ast|.

        .. describe:: ast_operator_sgr

            The :term:`SGR value` given to |token_operator| in an |ast|.

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

    NO_COLOR

        This environment variable can toggle :term:`on or off <boolean value>` ANSI output for all
        `supporting software <https://no-color.org>`_.

.. glossary::

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
