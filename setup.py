import distutils.command.build
import setuptools
import setuptools.command.develop
import setuptools.command.easy_install
import setuptools.command.install_lib

import itertools
import os
import re


class BuildPTH(distutils.command.build.build):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "pretty.pth")
        dest = os.path.join(self.build_lib, os.path.basename(path))
        self.copy_file(path, dest)


class DevelopPTH(setuptools.command.develop.develop):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "pretty.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)


class EasyInstallPTH(setuptools.command.easy_install.easy_install):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "pretty.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)


class InstallLibPTH(setuptools.command.install_lib.install_lib):
    def run(self):
        super().run()

        path = os.path.join(os.path.dirname(__file__), "pretty.pth")
        dest = os.path.join(self.install_dir, os.path.basename(path))
        self.copy_file(path, dest)

        self.outputs = [dest]

    def get_outputs(self):
        return itertools.chain(super().get_outputs(), self.outputs)


cmdclass = {
    "build": BuildPTH,
    "develop": DevelopPTH,
    "easy_insall": EasyInstallPTH,
    "install_lib": InstallLibPTH,
}

with open("docs/requirements.txt", "r") as stream:
    extras_require_docs = stream.read().splitlines()

extras_require = {
    "docs": extras_require_docs,
}

packages = setuptools.find_packages()

_version_regex = r"^version(?:\s*:\s*str)?\s*=\s*('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"

with open("pretty/__init__.py") as stream:
    match = re.search(_version_regex, stream.read(), re.MULTILINE)

if not match:
    raise RuntimeError("could not find version")

version = match.group(2)

if match.group(3) is not None:
    try:
        import subprocess

        process = subprocess.Popen(["git", "rev-list", "--count", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += out.decode("utf-8").strip()

        process = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE)
        out, _ = process.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception as e:
        pass


setuptools.setup(
    author="ShineyDev",
    author_email="contact@shiney.dev",
    cmdclass=cmdclass,
    description="A Python library with practical APIs for prettier output.",
    extras_require=extras_require,
    include_package_data=True,
    license="Apache Software License",
    name="pretty",
    packages=packages,
    python_requires=">=3.8.0",
    url="https://github.com/ShineyDev/pretty",
    version=version,
)
