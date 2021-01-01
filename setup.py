import itertools
import os

from distutils.core import setup
from distutils.command.build import build
from setuptools.command.develop import develop
from setuptools.command.easy_install import easy_install
from setuptools.command.install_lib import install_lib


class BuildPTH(build):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "prettify_exceptions_hook.pth")
        dest = os.path.join(self.build_lib, os.path.basename(path))
        self.copy_file(path, dest)


class DevelopPTH(develop):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "prettify_exceptions_hook.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)


class EasyInstallPTH(easy_install):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "prettify_exceptions_hook.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)


class InstallLibPTH(install_lib):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "prettify_exceptions_hook.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)

        self.outputs = [dest]

    def get_outputs(self):
        return itertools.chain(super().get_outputs(), self.outputs)


setup(
    author="ShineyDev",
    # https://github.com/pytest-dev/pytest-cov/blob/master/setup.py
    cmdclass={
        "build": BuildPTH,
        "develop": DevelopPTH,
        "easy_insall": EasyInstallPTH,
        "install_lib": InstallLibPTH,
    },
    license="Apache Software License",
    name="prettify.py",
    packages=["prettify_exceptions"],
    url="https://github.com/ShineyDev/prettify.py",
)
