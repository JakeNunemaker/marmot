"""Agent based process modeling using _simpy."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from ._core import ge, gt, le, lt, true, false
from .agent import Agent, process
from .object import Object
from ._version import get_versions
from .environment import Environment

__version__ = get_versions()["version"]
del get_versions
