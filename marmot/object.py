"""Object base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


class Object:
    """Base object class."""

    def __init__(self, name):
        """
        Creates an instance of `Object`. At instantiation the object is not
        assigned to an `Environment` and must be registered with one before it
        can be interacted with.

        Parameters
        ----------
        name : str
            Name of object.
        """

        self.name = name
        self._env = None

    def __repr__(self):
        return self.name

    @property
    def env(self):
        """Returns the active environment of the instance."""

        return self._env

    @env.setter
    def env(self, env):
        """
        Sets the active environment for instance.

        Parameters
        ----------
        env : `Environment`
            Environment to be registered to.

        Raises
        ------
        AlreadyRegistered
        """

        if env is None:
            self._env = env
            return

        elif self._env:
            raise AlreadyRegistered(self)

        self._env = env


class AlreadyRegistered(Exception):
    """Error for instances that are already registered with an environment."""

    def __init__(self, instance):
        """
        Creates an instance of AlreadyRegistered.

        Parameters
        ----------
        instance : `Object` | `Agent`
            Previously registered instance.
        """

        self.instance = instance
        self.message = (
            f"Instance '{instance}' is already registered with "
            f"'{instance.env}'."
        )

    def __str__(self):
        return self.message
