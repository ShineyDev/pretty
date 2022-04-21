Versioning
==========

This document outlines the versioning of the project.


Guarantees
----------

This project follows the |semver| principle.

    Given a version number MAJOR.MINOR.PATCH, increment the:

    - MAJOR version when you make incompatible API changes,
    - MINOR version when you add functionality in a compatible manner, and
    - PATCH version when you make compatible bug fixes.

.. important::

    Incompatible changes apply only to stable documented APIs.


Examples
--------

.. note::

    The following examples are non-exhaustive.


Incompatible
~~~~~~~~~~~~

- Removing an API.
- Renaming an API without providing an alias.


Compatible
~~~~~~~~~~

- Modifying an undocumented API.
- Modifying the behavior of an API to fix a bug.
