"""Distribution setup."""

import os

from setuptools import setup

import versioneer

ROOT = os.path.abspath(os.path.dirname(__file__))

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="Marmot",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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
        "pytest>=5.1",
        "pytest-cov",
    ],
    test_suite="pytest",
    tests_require=["pytest", "pytest-xdist", "pytest-cov"],
)
