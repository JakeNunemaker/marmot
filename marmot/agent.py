"""Agent base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from math import ceil
from functools import wraps

from .object import Object
from ._exceptions import (
    StateExhausted,
    WindowNotFound,
    AgentNotRegistered,
    AgentAlreadyScheduled,
)


def process(func):
    """
    Process decorator for `Agent` class.

    Parameters
    ----------
    func : method
        Function to be wrapped.

    Raises
    ------
    AgentNotRegistered
    AgentAlreadyScheduled
    """

    @wraps(func)
    def wrapper(agent, *args, **kwargs):

        env = getattr(agent, "env", None)
        if env is None:
            raise AgentNotRegistered(agent)

        if agent in env.scheduled_agents:
            raise AgentAlreadyScheduled(agent)

        try:
            return env.process(func(agent, *args, **kwargs), agent)

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

    @process
    def operational_window(self, duration, **kwargs):
        """
        Process method used to yield until a window of length `duration` that
        satisfies any valid operational constraints in kwargs.

        Parameters
        ----------
        duration : float | int
            Duration of required window.
            Rounded up to the nearest int.
        """

        try:
            delay = self.env.find_operational_window(ceil(duration), **kwargs)

        except WindowNotFound as e:
            e.agent = self
            raise e

        yield self.timeout(delay)

    @process
    def operational_delay(self, duration, **kwargs):
        """
        Process method used to yield for accumulated operational delays
        associated with an operation of length `duration` and any valid
        operational constraints found in kwargs.

        Parameters
        ----------
        duration : float | int
            Duration of operation.
            Rounded up to the nearest int.
        """
        try:
            delay = self.env.calculate_operational_delay(ceil(duration), **kwargs)

        except StateExhausted as e:
            e.agent = self
            raise e

        yield self.timeout(delay)

    @process
    def timeout(self, duration):
        """
        General timeout method used by an `Agent` to yield for the passage of
        time. Requires the agent to to be registered with an `Environment`.

        Parameters
        ----------
        duration : int | float
            Amount of time to yield for.

        Raises
        ------
        AgentNotRegistered
        """

        yield self.env.timeout(duration, agent=self)

    def submit_action_log(self, action, duration, **kwargs):
        """
        Submits a log representing a completed `action` performed over time
        `duration`. Additional log information can be passed through kwargs and
        will be passed to the environment logs.

        Parameters
        ----------
        action : str
            Performed action.
        duration : int | float
            Duration of action.

        Raises
        ------
        AgentNotRegistered
        """

        if self.env is None:
            raise AgentNotRegistered(self)

        else:
            payload = {
                **kwargs,
                "agent": str(self),
                "action": action,
                "duration": float(duration),
            }

            self.env._submit_log(payload, level="ACTION")

    def submit_debug_log(self, **kwargs):
        """
        Submits a generic log used for debugging processes.

        Raises
        ------
        AgentNotRegistered
        """

        if self.env is None:
            raise AgentNotRegistered(self)

        else:
            payload = {**kwargs, "agent": str(self)}

            self.env._submit_log(payload, level="DEBUG")
