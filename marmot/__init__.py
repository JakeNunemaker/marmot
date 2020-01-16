"""Agent based process modeling using SimPy."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import os

from ._core import ge, gt, le, lt, true, false
from .agent import Agent, process
from .object import Object
from .environment import Environment

ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.abspath(os.path.join(ROOT, "../VERSION"))) as version_file:
    VERSION = version_file.read().strip()


__version__ = VERSION
