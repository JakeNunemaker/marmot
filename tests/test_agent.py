"""Tests for the `marmot.Agent` class and `process` decorator."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import simpy
import pytest

from marmot import lt, true
from marmot._exceptions import (
    StateExhausted,
    WindowNotFound,
    AgentNotRegistered,
    AgentAlreadyScheduled,
)


def test_creation(ExampleAgent):

    agent = ExampleAgent()
    assert str(agent) == agent.name == "Test Agent"

    agent = ExampleAgent("Other Agent")
    assert str(agent) == agent.name == "Other Agent"


def test_unregistered_agent(env, ExampleAgent):

    agent = ExampleAgent()

    with pytest.raises(AgentNotRegistered):
        agent.pause_then_perform(5, 10)


def test_single_agent_processing(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.pause_then_perform(5, 10)

    env.run()
    assert env.now == 15


def test_multiple_agent_processing(env, ExampleAgent):

    agent1 = ExampleAgent("Agent 1")
    agent2 = ExampleAgent("Agent 2")
    env.register(agent1)
    env.register(agent2)

    agent1.pause_then_perform(5, 10)
    agent2.pause_then_perform(10, 10)

    env.run()
    assert env.now == 20


def test_processing_restart(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.pause_then_perform(5, 10)

    env.run()
    assert env.now == 15

    agent.pause_then_perform(5, 5)
    env.run()
    assert env.now == 25


def test_initialize_method(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.initialize()

    env.run()
    assert env.now == 15


def test_decorated_initialize_method(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.initialize_with_decorator()

    env.run()
    assert env.now == 15


def test_event_trigger(env, ExampleAgent):

    agent1 = ExampleAgent("Agent 1")
    agent2 = ExampleAgent("Agent 2")
    env.register(agent1)
    env.register(agent2)

    event = simpy.Event(env)

    agent1.wait_for_event(event, 25)
    agent2.trigger_event_after(event, 25)

    env.run()
    assert env.now == 50


def test_agent_already_scheduled(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.pause_then_perform(5, 10)

    with pytest.raises(AgentAlreadyScheduled):
        agent.pause(10)


def test_unsuspendable_task(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.task("Task", 4, constraints={"temp": lt(70)})
    env.run()
    assert env.now == 4

    agent.task("Task", 4, constraints={"temp": lt(100), "workday": true()})
    env.run()
    assert env.now == 10

    assert len(env.logs) == 3
    assert len(env.actions) == 3

    with pytest.raises(WindowNotFound) as excinfo:
        agent.task("Task", 10, constraints={"temp": lt(100)})
        env.run()

        assert excinfo.value.agent == agent


def test_suspendable_task(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.task("Task", 4, constraints={"temp": lt(70)}, suspendable=True)
    env.run()
    assert env.now == 4

    agent.task(
        "Task", 8, constraints={"temp": lt(100), "workday": true()}, suspendable=True
    )
    env.run()
    assert env.now == 20

    assert len(env.logs) == 5
    assert len(env.actions) == 5

    with pytest.raises(StateExhausted) as excinfo:
        agent.task("Task", 20, constraints={"temp": lt(70)}, suspendable=True)
        env.run()

        assert excinfo.value.agent == agent
