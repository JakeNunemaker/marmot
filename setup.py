"""Distribution setup."""

import os

from setuptools import setup, find_packages

import versioneer

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="Marmot",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["numpy", "simpy-agents"],
    extras_requires={
        "dev": ["pre-commit", "black", "isort", "pytest>=5.1", "pytest-cov"]
    },
    test_suite="pytest",
    tests_require=["pytest", "pytest-cov"],
)
