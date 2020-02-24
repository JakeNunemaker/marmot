"""Environment base class for marmot process modeling."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import itertools
from math import ceil

import numpy as np

import _simpy

from ._core import Constraint
from .agent import Agent
from .object import Object
from ._exceptions import (
    StateExhausted,
    WindowNotFound,
    ActionMissingKeys,
    RegistrationFailed,
    RegistrationConflict,
)


class Environment(_simpy.Environment):
    """Base environment class."""

    _action_required = ["agent", "action", "duration"]

    def __init__(self, name="Environment", state=None):
        """
        Creates an instance of Environment.

        Parameters
        ----------
        name : str
            Environment name.
            Default: 'Environment'
        state : array-like
            Time series representing the state of the environment throughout
            time or iterations.
        """

        super().__init__()

        self.name = name
        self.state = state
        self._logs = []
        self._agents = {}
        self._objects = []

    def __repr__(self):
        return self.name

    def _submit_log(self, payload, level):
        """
        Accepts a log `payload`, inserts the `level` and appends it to
        `self._logs`. If the level is 'ACTION', the action log is validated
        with `self._validate_action` before being added to the log list.

        Parameters
        ----------
        payload : dict
            Log data.
        level : str
        """

        payload["level"] = level
        if level == "ACTION":
            self._validate_action(payload)

        stamped = self._timestamp_log(payload)
        self._logs.append(stamped)

    def _validate_action(self, payload):
        """
        Validates an action log payload against `self._action_required`.

        Parameters
        ----------
        payload : dict
            Log data.
        """

        missing = set(self._action_required).difference(set(payload.keys()))
        if missing:
            raise ActionMissingKeys(payload, missing)

    def _timestamp_log(self, payload):
        """
        Adds the environment timestamp to an acceptable log `payload`.

        Parameters
        ----------
        payload : dict
            Log data.
        """

        payload["time"] = self.now
        return payload

    @property
    def state(self):
        """
        Returns forecast of `self.state`, starting at `ceil(self.now)`.
        """

        return self._state[ceil(self.now) :]

    @state.setter
    def state(self, data):
        """
        Sets the state data for the environment.

        Parameters
        ----------
        data : np.ndarray | None
        """

        if data is None:
            self._state = np.recarray(shape=(0,), dtype=[])
            return

        elif not isinstance(data, np.ndarray):
            raise TypeError(f"'state' data type '{type(data)}' not supported.")

        self._state = data

    def find_operational_window(self, n, constraints):
        """
        Finds the first window of length `n` that satisfies any valid
        conditions in kwargs. Conditions should be of type `Condition` from
        `marmot._core` and are applied the array corresponding to their key.
        This method can be used to calculate the delay associated with
        operations that can not be suspended.

        Examples
        --------
        - `n=5, windspeed=gt(10)` will calculate the delay until the first
        window of length 5 where all values in `self.state['windspeed']` are
        greater than 10.

        Parameters
        ----------
        n : int
            Length of required operational window.
        constraints : dict
            Dictionary of `Constraints` applied to `self.env.state` columns
            Format:
            - Key: name corresponding to column in `self.state`.
            - Value: `Constraint` to be applied.

        Returns
        -------
        delay : int
            Duration of delay until operational window begins.
        """

        if not self.state.size > 0:
            return 0

        valid = self._find_valid_constraints(**constraints)
        forecast = self._apply_constraints(self.state, valid)
        delay = self._find_first_window(forecast, n)

        if delay is None:
            raise WindowNotFound(n, **valid)

        return delay

    def calculate_operational_delays(self, n, constraints):
        """
        Calculates the accumulated operational delay associated with an
        operation of length `n` and any valid conditions in kwargs. Conditions
        should be of type `Condition` from `marmot._core` and are applied the
        array corresponding to their key. This method can be used to calculate
        the delay associated with operations that can be suspended.

        Examples
        --------
        - `n=5, windspeed=gt(10)` will identify any delays during an operation
        of length 5 where `self.state['windspeed']` must be greater than 10.

        Parameters
        ----------
        n : int
            Operation length.
        constraints : dict
            Dictionary of `Constraints` applied to `self.env.state` columns
            Format:
            - Key: name corresponding to column in `self.state`.
            - Value: `Constraint` to be applied.

        Returns
        -------
        durations : list
            List of delays and operation times.
        """

        if not self.state.size > 0:
            return [n]

        valid = self._find_valid_constraints(**constraints)
        forecast = self._apply_constraints(self.state, valid)
        durations = self._count_delays(forecast, n)

        if durations is None:
            raise StateExhausted(len(self._state), **valid)

        return durations

    def _find_valid_constraints(self, **kwargs):
        """
        Finds any constraints in `kwargs` where the key matches a column name
        in `self.state` and the value type is `Constraint`.

        Returns
        -------
        valid : dict
            Valid constraints that apply to a column in `self.state`.
        """

        keys = set(self.state.dtype.names).intersection(set(kwargs.keys()))
        valid = {
            k: v for k, v in kwargs.items() if k in keys and isinstance(v, Constraint)
        }

        return valid

    @staticmethod
    def _apply_constraints(arr, constraints):
        """
        Applies `constraints` to `arr`, returning a boolean array
        representing whether an operation can be processed for each step.

        Parameters
        ----------
        arr : np.ndarray
        constraints : dict
            Dictionary of `arr` column names and respective constraints.
            Format:
            - Key: name corresponding to column in `arr`.
            - Value: `Constraint` to be applied.

        Returns
        -------
        arr : np.ndarray
            Boolean array representing whether an operation can be processed.
        """

        if constraints:
            _list = [v(arr[k]) for k, v in constraints.items()]
            arr = np.all(_list, axis=0)

            return arr

        else:
            return np.repeat(True, arr.shape)

    @staticmethod
    def _count_delays(arr, n):
        """
        Count the accumulated `False` values in `arr` until an operation of
        length `n` can be completed.

        Parameters
        ----------
        arr : np.ndarray
            Boolean array.
        n : int
            Operation length in index steps.

        Returns
        -------
        durations : list | None
            List of delays and operation times or `None` if the required
            operation length `n` is not met.
        """

        durations = []
        for val, g in itertools.groupby(arr):
            l = len(list(g))

            if val == True:
                if l >= n:
                    durations.append(n)
                    return durations

                else:
                    durations.append(l)
                    n -= l

            else:
                durations.append(l)

        return None

    @staticmethod
    def _find_first_window(arr, n):
        """
        Find first window of `True` values, length `n` within `arr`.

        Parameters
        ----------
        arr : np.ndarray
            Boolean array.
        n : int
            Width of window in index steps.

        Returns
        -------
        delay : int | None
            Duration of delay until operational window begins or None if a
            window of length `n` is not found.
        """

        arr = np.append(arr, False)
        false = np.where(~arr)[0]

        if false.size == 0:
            delay = 0

        elif false[0] >= n:
            delay = 0

        else:
            diff = np.where((false[1:] - false[:-1] - 1) >= n)[0]

            try:
                delay = false[diff[0]] + 1

            except IndexError:
                delay = None

        return delay

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

        Raises
        ------
        RegistrationFailed
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

        Raises
        ------
        RegistrationConflict
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

    @property
    def logs(self):
        """Returns list of all log payloads."""

        return self._logs

    @property
    def actions(self):
        """Returns list of action log payloads."""

        return [l for l in self._logs if l["level"] == "ACTION"]
