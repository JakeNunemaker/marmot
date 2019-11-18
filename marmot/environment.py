"""Environment base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__credits__ = ""
# __version__ = "0.0.1"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


from .agent import Agent
from .object import Object


class Environment:
    """Base environment class."""

    _agents = []
    _objects = []

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

        if isinstance(instance, Object):
            self._objects.append(instance)

        elif isinstance(instance, Agent):
            self._agents.append(instance)

        else:
            raise RegistrationFailed(instance)

    def deregister(self, instance):
        """
        Deregisters an instance from the environment, removing it from the list
        of currently activated instances.

        Parameters
        ----------
        instance : `Agent` | `Object`
            Instance to be registered.
        """

        pass

    @property
    def active_agents(self):
        """Returns list of currently registered agents."""

        return self._agents

    @property
    def active_objects(self):
        """Returns list of currently registered objects."""

        return self._objects


class RegistrationConflict(Exception):
    """Error for conflicting agent names."""

    def __init__(self, agent):
        """
        Creates an instance of RegistrationConflict.

        Parameters
        ----------
        agent : str
            Conflicting agent name.
        """

        self.message = f"'{agent}' is already registered to {self.name}."

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

        t = type(instance)
        self.message = f"'{i}', type '{t}' not recognized for registration."

    def __str__(self):
        return self.message
