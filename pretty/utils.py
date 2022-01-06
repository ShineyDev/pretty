import functools
import os
import re


_env_all = "PYTHONPRETTY"
_env_theme = "PYTHONPRETTYTHEME"
_env_traceback = "PYTHONPRETTYTRACEBACK"


_bool_map = {
    False: ["false", "0", "no", "n", "disable", "off"],
    True: ["true", "1", "yes", "y", "enable", "on"],
}


@functools.lru_cache
def environment_to_bool(name, default):
    try:
        value = os.environ[name]
    except KeyError:
        return default
    else:
        value = value.lower()

        for (boolean, values) in _bool_map.items():
            if value in values:
                return boolean

        return default


_default_theme = {
    "cap": "\u2514",
    "pipe": "\u2502",
    "comment": "32",
    "introspection": "35",
    "keyword": "34",
    "literal_bool": "34",
    "literal_int": "36",
    "literal_none": "94",
    "literal_str": "31",
    "path_substitutions": "",
}

_unicode_re = re.compile(r"u\+[0-9]{4}|U\+[0-9]{8}")


@functools.lru_cache
def environment_to_theme(name, default):
    try:
        value = os.environ[name]
    except KeyError:
        return default
    else:
        values = value.split("|")

        theme = _default_theme.copy()

        for value in values:
            try:
                name, value = value.split("=")
            except ValueError:
                pass
            else:
                name = name.lower().strip()
                value = value.strip()

                def _repl(match):
                    return chr(int(match.group(0)[2:], 16))

                value = re.sub(_unicode_re, _repl, value)

                theme[name] = value

        return theme


def wrap(wrapped):
    def decorator(wrapper):
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__name__ = wrapped.__name__
        wrapper.__qualname__ = wrapped.__qualname__

        return wrapper

    return decorator


__all__ = [
    "environment_to_bool",
    "environment_to_theme",
    "wrap",
]
