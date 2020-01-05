"""Distribution setup."""

import os

from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

with open("README.rst", "r") as fh:
    long_description = fh.read()

with open(os.path.join(ROOT, "VERSION")) as version_file:
    __version__ = version_file.read().strip()


setup(
    name="Marmot",
    version=__version__,
    description=long_description,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["marmot"],
    install_requires=[
        "simpy-agents @ http://github.com/JakeNunemaker/simpy-agents/tarball/master#egg=v0.1.0",
        "pyyaml",
        "pre-commit",
        "black",
        "isort",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
    ],
    test_suite="pytest",
    tests_require=["pytest", "pytest-xdist", "pytest-cov"],
)
