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
import traceback

from prettify_exceptions.formatter import DefaultFormatter


def is_hooked():
    # whether we are, or another package is, already hooked
    return sys.excepthook is not sys.__excepthook__

def create_excepthook(formatter):
    def excepthook(*args):
        print("".join(formatter.format_exception(*args)).strip())

    return excepthook

def hook(cls=DefaultFormatter, **kwargs):
    override_hook = kwargs.pop("override_hook", False)
    override_traceback = kwargs.pop("override_traceback", False)

    formatter = cls(**kwargs)

    if override_traceback:
        traceback.format_exc = formatter.format_exc
        traceback.format_exception = formatter.format_exception
        traceback.format_exception_only = formatter.format_exception_only
        traceback.format_list = formatter.format_list
        traceback.format_stack = formatter.format_stack
        traceback.format_tb = formatter.format_traceback

    if override_hook or not is_hooked():
        sys.excepthook = create_excepthook(formatter)
