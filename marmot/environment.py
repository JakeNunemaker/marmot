"""Environment base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from .agent import Agent
from .object import Object


class Environment:
    """Base environment class."""

    def __init__(self, name="Environment"):
        """
        Creates an instance of Environment.

        Parameters
        ----------
        name : str
            Environment name.
            Default: 'Environment'
        """

        self.name = name
        self._agents = {}
        self._objects = []

    def __repr__(self):
        return self.name

    def register(self, instance):
        """
        Registers an instance of `Agent` or `Object` to the environment. This
        process is required for an instance to interact with other instances.
        An instance of `Agent` type must be unique whereas an `Object` instance
        can be duplicated.

        Parameters
        ----------
        instance : `Agent` | `Object`
            Instance to be registered.
        """

        if isinstance(instance, Agent):
            self._register_agent(instance)

        elif isinstance(instance, Object):
            self._register_object(instance)

        else:
            raise RegistrationFailed(instance)

    def _register_agent(self, agent):
        """
        Agent registration process.

        Parameters
        ----------
        agent : `Agent`
            Agent to be registered.
        """

        if str(agent) in self._agents.keys():
            raise RegistrationConflict(self, agent)

        agent.env = self
        self._agents[str(agent)] = agent

    def _register_object(self, obj):
        """
        Object registration process.

        Parameters
        ----------
        obj : `Object`
            Object to be registered.
        """

        obj.env = self
        self._objects.append(obj)

    def deregister(self, name):
        """
        Deregisters an `Agent` from the environment, removing it from the list
        of currently reserved agent names.

        Parameters
        ----------
        name : str
            Agent to be deregistered.
        """

        agent = self._agents.pop(str(name), None)
        if agent is None:
            print(f"Agent '{name}' not found in active agents.")
            return

        agent.env = None
        print(f"Agent '{name}' deregistered from '{self.name}'.")

    @property
    def active_agents(self):
        """Returns list of currently registered agents."""

        return self._agents.values()

    @property
    def active_objects(self):
        """Returns list of currently registered objects."""

        return self._objects


class RegistrationConflict(Exception):
    """Error for conflicting agent names."""

    def __init__(self, env, agent):
        """
        Creates an instance of RegistrationConflict.

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
            f"'{self.env}' already has a registered agent with "
            f"name '{agent}'."
        )

    def __str__(self):
        return self.message


class RegistrationFailed(Exception):
    """Error for failed registrations."""

    def __init__(self, i):
        """
        Creates an instance of RegistrationFailed.

        Parameters
        ----------
        i : object
        """

        t = type(i)
        self.message = f"'{i}', type '{t}' not recognized for registration."

    def __str__(self):
        return self.message
