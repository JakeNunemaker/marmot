"""pytest.fixtures used in the marmot test package."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


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

    return Environment(name="Test Environment")
