"""Tests for the `marmot.Environment` class."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import pytest
from simpy.core import EmptySchedule

from marmot import Agent, Object, Environment
from marmot.object import AlreadyRegistered
from marmot.environment import RegistrationFailed, RegistrationConflict


def test_registration(env):

    obj = Object("Test Object")
    agent = Agent("Test Agent")

    env.register(obj)
    assert len(env._objects) == 1
    assert obj.env == env

    env.register(agent)
    assert len(env._agents) == 1
    assert agent.env == env


def test_failed_registration(env):

    with pytest.raises(RegistrationFailed):
        env.register("Invalid")


def test_registration_conflict(env):

    obj1 = Object("Test Object")
    obj2 = Object("Test Object")
    agent1 = Agent("Test Agent")
    agent2 = Agent("Test Agent")

    env.register(obj1)
    env.register(obj2)
    assert len(env._objects) == 2

    env.register(agent1)
    with pytest.raises(RegistrationConflict):
        env.register(agent2)


def test_deregistration_with_name(env):

    agent = Agent("Test Agent")

    env.register(agent)
    assert len(env._agents) == 1
    assert agent.env == env

    env.deregister("Test Agent")
    assert len(env._agents) == 0
    assert agent.env == None


def test_deregistration_with_instance(env):

    agent = Agent("Test Agent")

    env.register(agent)
    assert len(env._agents) == 1
    assert agent.env == env

    env.deregister(agent)
    assert len(env._agents) == 0
    assert agent.env == None


def test_unknown_deregistration(env):

    agent = Agent("Test Agent")

    env.register(agent)
    assert len(env._agents) == 1

    env.deregister("Unknown Agent")
    assert len(env._agents) == 1


def test_already_registered():

    env1 = Environment("Test Environment 1")
    env2 = Environment("Test Environment 2")
    agent = Agent("Test Agent")

    env1.register(agent)

    with pytest.raises(AlreadyRegistered):
        env2.register(agent)

    env1.deregister(agent)
    env2.register(agent)
    assert len(env2._agents) == 1


def test_scheduled_agents(env, ExampleAgent):

    agent1 = ExampleAgent("Agent 1")
    env.register(agent1)
    agent1.pause(10)

    assert len(env.scheduled_agents) == 1

    agent2 = ExampleAgent("Agent 2")
    env.register(agent2)
    agent2.pause(10)

    assert len(env.scheduled_agents) == 2
    assert agent1 in env.scheduled_agents
    assert agent2 in env.scheduled_agents


def test_scheduled_agents_completeness(env, ExampleAgent):

    agent1 = ExampleAgent("Agent 1")
    env.register(agent1)
    agent1.pause_then_perform(50, 20)

    agent2 = ExampleAgent("Agent 2")
    env.register(agent2)
    agent2.pause(100)

    agent3 = ExampleAgent("Agent 3")
    env.register(agent3)
    agent3.pause_then_perform(40, 60)

    while True:

        try:
            assert None not in env.scheduled_agents
            env.step()

        except EmptySchedule:
            break
