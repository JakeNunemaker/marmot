"""Agent base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from functools import wraps

from .object import Object


def process(func):
    """
    Process decorator for `Agent` class.

    Parameters
    ----------
    func : method
        Function to be wrapped.
    """

    @wraps(func)
    def wrapper(agent, *args, **kwargs):

        env = getattr(agent, "env", None)
        if env is None:
            raise AgentNotRegistered(agent)

        try:
            process = env.process(func(agent, *args, **kwargs))
            return process

        except ValueError:
            return

    return wrapper


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


class AgentNotRegistered(Exception):
    """Error for unregistered agents."""

    def __init__(self, agent):
        """
        Creates an instance of AgentNotRegistered.

        Parameters
        ----------
        agent : `Agent`
            Unregistered agent.
        """

        self.agent = agent
        self.message = f"Agent '{agent}' is not registered to an environment."

    def __str__(self):
        return self.message
