import os


boolean_map = {
    "1": True,
    "true": True,
    "on": True,
    "enable": True,
    "yes": True,
    "y": True,
    "0": False,
    "false": False,
    "off": False,
    "disable": False,
    "no": False,
    "n": False,
}


def environment_to_boolean(name, default):
    try:
        value = os.environ[name]
    except KeyError:
        return default
    else:
        try:
            return boolean_map[value.lower()]
        except KeyError:
            return default


# NOTE: SGR color values are HSV(x°, 30%, 100%) where;
#
#       x     SGR           name
#       ---   -----------   ---------
#       0     255;179;179   red
#       30    255;217;179   orange
#       60    255;255;179   yellow
#       90    217;255;179   lime
#       120   179;255;179   green
#       150   179;255;217   turquoise
#       180   179;255;255   cyan
#       210   179;217;255   blue
#       240   179;179;255   indigo
#       270   217;179;255   purple
#       300   255;179;255   magenta
#       330   255;179;217   pink
#
#       SGR grayscale values are HSV(0°, 0%, y%) where;
#
#       y     SGR           name
#       --    -----------   -----
#       10    26;26;26      black
#       50    128;128;128   gray
#       90    230;230;230   white
#
pretty_theme = {
    # colorizing abstract syntax trees
    "ast_comment_sgr": ("38;2;179;255;179", "39"),
    "ast_delimiter_sgr": ("38;2;128;128;128", "39"),
    "ast_keyword_sgr": ("38;2;179;179;255", "39"),
    "ast_operator_sgr": ("38;2;128;128;128", "39"),
    # customizing character display
    "char_cap": "\u2514",
    "char_pipe": "\u2502",
    "char_quote": "\u0022",
    # colorizing literal types
    "literal_bool_sgr": ("38;2;179;179;255", "39"),
    "literal_bytes_sgr": ("38;2;255;217;179", "39"),
    "literal_complex_sgr": ("38;2;179;255;255", "39"),
    "literal_ellipsis_sgr": ("38;2;128;128;128", "39"),
    "literal_float_sgr": ("38;2;179;255;255", "39"),
    "literal_int_sgr": ("38;2;179;255;255", "39"),
    "literal_none_sgr": ("38;2;179;179;255", "39"),
    "literal_str_sgr": ("38;2;255;217;179", "39"),
    # pretty.traceback
    "traceback_exception_sgr": ("38;2;255;179;179", "39"),
    "traceback_location_sgr": ("1", "22"),
    "traceback_introspection_sgr": ("38;2;255;179;255", "39"),
}


def wrap(wrapped):
    def decorator(wrapper):
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__name__ = wrapped.__name__
        wrapper.__qualname__ = wrapped.__qualname__

        return wrapper

    return decorator


__all__ = [
    "environment_to_boolean",
    "wrap",
]
