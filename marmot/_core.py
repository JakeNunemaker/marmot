"""Core functionality for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2020, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


class Constraint:
    pass


class gt(Constraint):
    def __init__(self, val):

        if isinstance(val, (int, float)) and not isinstance(val, bool):
            self.val = val

        else:
            raise TypeError(f"Constraint 'gt' requires a numeric input.")

    def __call__(self, arr):
        """
        Returns boolean array where `arr` > `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr > self.val

    def __repr__(self):

        return f" > {self.val}"


class ge(Constraint):
    def __init__(self, val):

        if isinstance(val, (int, float)) and not isinstance(val, bool):
            self.val = val

        else:
            raise TypeError(f"Constraint 'ge' requires a numeric input.")

    def __call__(self, arr):
        """
        Returns boolean array where `arr` >= `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr >= self.val

    def __repr__(self):

        return f" >= {self.val}"


class lt(Constraint):
    def __init__(self, val):

        if isinstance(val, (int, float)) and not isinstance(val, bool):
            self.val = val

        else:
            raise TypeError(f"Constraint 'lt' requires a numeric input.")

    def __call__(self, arr):
        """
        Returns boolean array where `arr` < `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr < self.val

    def __repr__(self):

        return f" < {self.val}"


class le(Constraint):
    def __init__(self, val):

        if isinstance(val, (int, float)) and not isinstance(val, bool):
            self.val = val

        else:
            raise TypeError(f"Constraint 'le' requires a numeric input.")

    def __call__(self, arr):
        """
        Returns boolean array where `arr` <= `val`.

        Parameters
        ----------
        arr : array-like
        """

        return arr <= self.val

    def __repr__(self):

        return f" <= {self.val}"


class false(Constraint):
    def __init__(self):
        pass

    def __call__(self, arr):
        """
        Returns boolean array where `array` is `False`.

        Parameters
        ----------
        arr : array-like
        """

        return ~arr.astype(bool)

    def __repr__(self):

        return f" is False"


class true(Constraint):
    def __init__(self):
        pass

    def __call__(self, arr):
        """
        Returns boolean array where `array` is `True`.

        Parameters
        ----------
        arr : array-like
        """

        return arr.astype(bool)

    def __repr__(self):

        return f" is True"
