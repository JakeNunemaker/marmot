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
    def timeout(self, time):
        """
        General timeout method used by an `Agent` to wait for the passage of
        time. Requires the agent to to be registered with an `Environment`.

        Parameters
        ----------
        time : int | float
            Amount of time to wait for.

        Raises
        ------
        AgentNotRegistered
        """

        if self.env is None:
            raise AgentNotRegistered(self)

        else:
            yield self.env.timeout(time, agent=self)

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


class AgentAlreadyScheduled(Exception):
    """Error for agents scheduled more than once."""

    def __init__(self, agent):
        """
        Creates an instance of AgentAlreadyScheduled.

        Parameters
        ----------
        agent : `Agent`
            Overscheduled agent.
        """

        self.agent = agent
        self.message = f"Agent '{agent}' is already scheduled."

    def __str__(self):
        return self.message
