import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretalx-orcid",
    version="0.0.8",
    description="Gather speaker data from ORCID",
    long_description=long_description,
    url="https://pretalx.com/pretalx/pretalx-orcid",
    author="Tobias Kunze",
    author_email="r@rixx.de",
    license="Apache Software License",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretalx.plugin]
pretalx_orcid=pretalx_orcid:PretalxPluginMeta
""",
)
