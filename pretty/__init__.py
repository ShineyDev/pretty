import collections
import sys

from pretty import utils
from pretty import traceback


__all__ = []


_VersionInfo = collections.namedtuple("_VersionInfo", "major minor micro release serial")

version = "2.0.0a"
version_info = _VersionInfo(2, 0, 0, "alpha", 0)


def main():
    # NOTE: This function is called at every Python startup. Its impact
    #       should thus be kept to a minimum.
    #
    #       See https://docs.python.org/3/library/site.html.

    all = utils.environment_to_bool("PYTHONPRETTY", None)

    if all is False:
        return

    theme = utils.environment_to_theme("PYTHONPRETTYTHEME", None)

    if all or utils.environment_to_bool("PYTHONPRETTYTRACEBACK", False):
        try:
            traceback.hook(theme=theme)
        except BaseException as e:
            print("ERROR:pretty:failed to hook pretty.traceback, see traceback.print_last()")
            sys.last_type, sys.last_value, sys.last_traceback = type(e), e, e.__traceback__
