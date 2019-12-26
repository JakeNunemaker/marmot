"""Tests for `Agent` base class."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import pytest

from marmot import Agent, Environment, process
from marmot.agent import AgentNotRegistered


class TestAgent(Agent):
    def __init__(self, name="Test Agent"):
        """
        Creates an instance of `TestAgent`.

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

        yield self.env.timeout(time)

    @process
    def perform(self, time):
        """
        Process method for performing this agent's action.

        Paramaters
        ----------
        time : int | float
            Time to puase for.
        """

        yield self.env.timeout(time)

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


def test_creation():

    agent = TestAgent()
    assert str(agent) == agent.name == "Test Agent"

    agent = TestAgent("Other Agent")
    assert str(agent) == agent.name == "Other Agent"


def test_unregistered_agent():

    env = Environment("Test Environment")
    agent = TestAgent()

    with pytest.raises(AgentNotRegistered):
        agent.pause_then_perform(5, 10)


def test_single_agent_processing():

    env = Environment("Test Environment")
    agent = TestAgent()
    env.register(agent)

    agent.pause_then_perform(5, 10)

    env.run()
    assert env.now == 15


def test_multiple_agent_processing():

    env = Environment("Test Environment")
    agent1 = TestAgent("Agent 1")
    agent2 = TestAgent("Agent 2")
    env.register(agent1)
    env.register(agent2)

    agent1.pause_then_perform(5, 10)
    agent2.pause_then_perform(10, 10)

    env.run()
    assert env.now == 20


def test_processing_restart():

    env = Environment("Test Environment")
    agent = TestAgent()
    env.register(agent)

    agent.pause_then_perform(5, 10)

    env.run()
    assert env.now == 15

    agent.pause_then_perform(5, 5)
    env.run()
    assert env.now == 25


def test_initialize_method():

    env = Environment("Test Environment")
    agent = TestAgent()
    env.register(agent)

    agent.initialize()

    env.run()
    assert env.now == 15


def test_decorated_initialize_method():

    env = Environment("Test Environment")
    agent = TestAgent()
    env.register(agent)

    agent.initialize_with_decorator()

    env.run()
    assert env.now == 15
