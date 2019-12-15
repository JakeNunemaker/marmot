"""Agent base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from .object import Object


class Agent(Object):
    """Base agent class."""

    def __init__(self, name):
        """
        Creates an instance of `Agent`. At instantiation the agent is not
        assigned to an `Environment` and must be registered with one before it
        can perform any operations.

        Parameters
        ----------
        name : str
            Name of agent.
        """

        super().__init__(name)
