import collections

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

    all = utils.environment_to_bool(utils._env_all, None)

    if all is False:
        return

    theme = utils.environment_to_theme(utils._env_theme, utils._default_theme)

    if all or utils.environment_to_bool(utils._env_traceback, False):
        traceback.hook(theme=theme)
