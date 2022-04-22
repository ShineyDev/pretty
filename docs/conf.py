import os
import re
import sys


sys.path.insert(0, os.path.abspath(".."))


author = "ShineyDev"
project = "pretty"

copyright = f"2020-present, {author}"

_version_regex = r"^version(?:\s*:\s*str)?\s*=\s*('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"

with open("../pretty/__init__.py") as stream:
    match = re.search(_version_regex, stream.read(), re.MULTILINE)

release = "v" + match.group(2)
version = release

if match.group(3) is not None:
    try:
        import subprocess

        process = subprocess.Popen(["git", "rev-list", "--count", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            release += out.decode("utf-8").strip()

        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            release += "+g" + out.decode("utf-8").strip()
    except (Exception) as e:
        pass


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib_trio",
    "sphinx_rtd_theme",
]

autodoc_member_order = "groupwise"
autodoc_typehints = "none"

extlinks = {
    "issue": (f"https://github.com/{author}/{project}/issues/%s", "#"),
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}


highlight_language = "none"
pygments_style = "friendly"
root_doc = "index"
rst_prolog = """

.. |iter| replace:: This function returns an |iter_link|_.
.. |iter_link| replace:: iterator
.. _iter_link: https://docs.python.org/3/glossary.html#term-iterator

.. |semver| replace:: |semver_link|_
.. |semver_link| replace:: semantic versioning
.. _semver_link: https://semver.org/

.. |sgr| replace:: |sgr_link|_
.. |sgr_link| replace:: SGR
.. _sgr_link: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

.. |token_comment| replace:: |token_comment_link|_
.. |token_comment_link| replace:: comment tokens
.. _token_comment_link: https://docs.python.org/3/reference/lexical_analysis.html#comments

.. |token_delimiter| replace:: |token_delimiter_link|_
.. |token_delimiter_link| replace:: delimiter tokens
.. _token_delimiter_link: https://docs.python.org/3/reference/lexical_analysis.html#delimiters

.. |token_keyword| replace:: |token_keyword_link|_
.. |token_keyword_link| replace:: keyword tokens
.. _token_keyword_link: https://docs.python.org/3/reference/lexical_analysis.html#keywords

.. |token_name| replace:: |token_name_link|_
.. |token_name_link| replace:: name tokens
.. _token_name_link: https://docs.python.org/3/reference/lexical_analysis.html#identifiers

.. |token_operator| replace:: |token_operator_link|_
.. |token_operator_link| replace:: operator tokens
.. _token_operator_link: https://docs.python.org/3/reference/lexical_analysis.html#operators

.. |token_soft_keyword| replace:: |token_soft_keyword_link|_
.. |token_soft_keyword_link| replace:: soft keyword tokens
.. _token_soft_keyword_link: https://docs.python.org/3/reference/lexical_analysis.html#soft-keywords
"""
source_suffix = ".rst"


html_favicon = "favicon.svg"
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "includehidden": False,
    "navigation_depth": -1,
    "prev_next_buttons_location": None,
    "titles_only": True,
}
html_title = f"{project} {version}"
