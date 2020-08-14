"""
/prettify_exceptions/__init__.py

    Copyright (c) 2020 ShineyDev

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import sys

from prettify_exceptions.formatter import DefaultFormatter


def is_hooked():
    # whether we are, or another package is, already hooked
    return sys.excepthook is not sys.__excepthook__

def create_excepthook(formatter):
    def excepthook(*args):
        print("".join(formatter.format_exception(*args)).strip())

    return excepthook

def hook(cls=DefaultFormatter, **kwargs):
    override = kwargs.pop("override_hook", False)
    if not is_hooked() or override:
        sys.excepthook = create_excepthook(cls(**kwargs))
