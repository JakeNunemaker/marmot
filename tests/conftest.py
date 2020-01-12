"""pytest.fixtures used in the marmot test package."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import numpy as np
import pytest

from marmot import Agent, Environment, process


@pytest.fixture
def ExampleAgent():
    class _Agent(Agent):
        def __init__(self, name="Test Agent"):
            """
            Creates an instance of `ExampleAgent`.

            Parameters
            ----------
            name : str
                Name, default: 'Test Agent'
            """

            super().__init__(name)

        @process
        def pause(self, time):
            """
            Process method used to pause for input time.

            Paramaters
            ----------
            time : int | float
                Time to puase for.
            """

            yield self.timeout(time)
            self.submit_action_log("Pause", time)

        @process
        def perform(self, time):
            """
            Process method for performing this agent's action.

            Paramaters
            ----------
            time : int | float
                Time to puase for.
            """

            self.submit_debug_log(status="Starting")
            yield self.timeout(time)
            self.submit_action_log("Perform", time, status="Successful")

        @process
        def pause_then_perform(self, a, b):
            """A series of tasks that the agent must complete."""

            yield self.pause(a)
            yield self.perform(b)

        def initialize(self):
            """An initialize method."""

            self.pause_then_perform(5, 10)

        @process
        def initialize_with_decorator(self):
            """An initialize method."""

            self.pause_then_perform(5, 10)

        @process
        def wait_for_event(self, event, time):
            """An example waiting function."""

            start = self.env.now
            self.submit_debug_log(status="StartWaiting")
            yield event
            waited = self.env.now - start
            self.submit_action_log("WaitForEvent", waited, status="DoneWaiting")

            yield self.perform(time)

        @process
        def trigger_event_after(self, event, time):

            yield self.pause(time)
            event.succeed()

    return _Agent


@pytest.fixture
def env():

    data = np.array(
        [
            (60, False),
            (65, False),
            (67, False),
            (68, False),
            (70, False),
            (72, False),
            (78, True),
            (82, True),
            (86, True),
            (90, True),
            (98, True),
            (99, True),
            (100, True),
            (101, True),
            (104, True),
            (105, True),
            (106, True),
            (103, True),
            (99, True),
            (93, True),
            (87, False),
            (84, False),
            (77, False),
            (74, False),
        ],
        dtype=[("temp", "i8"), ("workday", "b")],
    )

    return Environment(name="Test Environment", state=data)


@pytest.fixture
def min_env():

    return Environment(name="Test Environment")
