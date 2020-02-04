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
    def task(self, name, duration, constraints={}, suspendable=False, **kwargs):
        """
        Represents a task of length `duration` to be completed by the agent.
        Requires the agent to be registered with an `Environment`.

        The `suspendable` flag controls how operational delays are handled
        during the task. If `False`, a window that satisfies all `constraints`
        must be found before the agent can begin the task. If `True`, the agent
        will start the task at the first valid timestep and pause when any
        `constraints` are violated.

        Parameters
        ----------
        name : str
            Name of task to complete. Used for submitting action logs.
        duration : float | int
            Duration of the task.
            Rounded up to the nearest int.
        constraints : dict
            Dictionary of `Constraints` applied to `self.env.state` columns
            Format:
            - Key: name corresponding to column in `self.state`.
            - Value: `Constraint` to be applied.
        suspendable : bool
            Controls if the task can be suspended during operation.
        """

        if suspendable:
            try:
                durations = self.env.calculate_operational_delays(duration, constraints)

            except StateExhausted as e:
                e.agent = self
                raise e

            if len(durations) % 2 != 0:
                first = durations.pop(0)
                yield self.timeout(first)
                self.submit_action_log(str(name), first, **kwargs)

            for i, d in enumerate(durations):
                yield self.timeout(d)

                if i % 2 == 0:
                    self.submit_action_log("Delay", d, **kwargs)

                else:
                    self.submit_action_log(str(name), d, **kwargs)

        else:
            try:
                delay = self.env.find_operational_window(ceil(duration), constraints)

            except WindowNotFound as e:
                e.agent = self
                raise e

            if delay:
                yield self.timeout(delay)
                self.submit_action_log("Delay", delay, **kwargs)

            yield self.timeout(duration)
            self.submit_action_log(str(name), duration, **kwargs)

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
