"""Core functionality for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2020, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


def gt(val):
    def inner(arr):
        """
        Returns boolean array where `arr` > `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr > val

    return inner


def ge(val):
    def inner(arr):
        """
        Returns boolean array where `arr` >= `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr >= val

    return inner


def lt(val):
    def inner(arr):
        """
        Returns boolean array where `arr` < `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr < val

    return inner


def le(val):
    def inner(arr):
        """
        Returns boolean array where `arr` <= `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr <= val

    return inner


def false():
    def inner(arr):
        """
        Returns boolean array where `array` is `False`.

        Parameters
        ----------
        arr : array-like
        """

        return ~arr

    return inner


def true():
    def inner(arr):
        """
        Returns boolean array where `array` is `True`.

        Parameters
        ----------
        arr : array-like
        """

        return arr

    return inner
