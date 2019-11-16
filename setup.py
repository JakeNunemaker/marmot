from setuptools import setup

import marmot

with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="Marmot",
    version=marmot.__version__,
    description=long_description,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["marmot"],
    install_requires=[
        "simpy",
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