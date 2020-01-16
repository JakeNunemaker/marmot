"""Custom exceptions used in Marmot."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2020, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


class ActionMissingKeys(Exception):
    """Error for missing keys in an action log."""

    def __init__(self, payload, missing):
        """
        Creates an instance of `ActionMissingKeys`.

        Parameters
        ----------
        payload : dict
            Log data.
        missing : list
            Missing keys.
        """

        self.payload = payload
        self.missing = missing
        self.message = f"Action log {payload} is missing required key(s) {missing}."

    def __str__(self):
        return self.message


class RegistrationConflict(Exception):
    """Error for conflicting agent names."""

    def __init__(self, env, agent):
        """
        Creates an instance of `RegistrationConflict`.

        Parameters
        ----------
        env : `Environment`
            Environment where conflict occured.
        agent : `Agent`
            Conflicting agent.
        """

        self.env = env
        self.agent = agent
        self.message = (
            f"'{self.env}' already has a registered agent with " f"name '{agent}'."
        )

    def __str__(self):
        return self.message


class RegistrationFailed(Exception):
    """Error for failed registrations."""

    def __init__(self, i):
        """
        Creates an instance of `RegistrationFailed`.

        Parameters
        ----------
        i : object
        """

        t = type(i)
        self.message = f"'{i}', type '{t}' not recognized for registration."

    def __str__(self):
        return self.message


class AgentNotRegistered(Exception):
    """Error for unregistered agents."""

    def __init__(self, agent):
        """
        Creates an instance of `AgentNotRegistered`.

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
        Creates an instance of `AgentAlreadyScheduled`.

        Parameters
        ----------
        agent : `Agent`
            Overscheduled agent.
        """

        self.agent = agent
        self.message = f"Agent '{agent}' is already scheduled."

    def __str__(self):
        return self.message


class WindowNotFound(Exception):
    """
    Error for operational window that can't be satisfied at any point in the
    state forecast.
    """

    def __init__(self, duration, agent=None, **constraints):
        """
        Creates an instance of `WindowNotFound`.

        Parameters
        ----------
        duration : int | float
            Duration of required window.
        agent : str
            Name of agent performing action.
        """

        self.agent = agent
        self.duration = duration
        self._constraints = "".join([f"\n\t\t'{k}{v}'" for k, v in constraints.items()])

        self.message = (
            f"An operational window of length {duration} was not found that "
            f"satisfies:"
        ) + self._constraints

    def __str__(self):

        if self.agent:
            return f"'{self.agent}': " + self.message

        else:
            return self.message


class StateExhausted(Exception):
    """Error raised at the end of state data."""

    def __init__(self, length, agent=None, **constraints):
        """
        Creates an instance of `StateExhausted`.

        Parameters
        ----------
        length : int
            Total number of elements in state data.
        """

        self.agent = agent
        self.length = length
        self._constraints = "".join([f"\n\t\t'{k}{v}'" for k, v in constraints.items()])

        self.message = (
            f"State data exhausted at element {length:,.0f}." + self._constraints
        )

    def __str__(self):

        if self.agent:
            return f"'{self.agent}': " + self.message

        else:
            return self.message
