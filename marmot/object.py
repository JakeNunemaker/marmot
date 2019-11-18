"""Object base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__credits__ = ""
# __version__ = "0.0.1"
__maintainer__ = "Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


class Object:
    """Base object class."""

    def __init__(self, name):
        """
        Creates an instance of Object.

        Parameters
        ----------
        name : str
            Name of object.
        """

        self.name = name
