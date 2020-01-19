"""Tests for the `marmot.Environment` class."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import numpy as np
import pytest
from simpy.core import EmptySchedule

from marmot import Agent, Object, Environment, lt, true
from marmot.agent import WindowNotFound
from marmot.object import AlreadyRegistered
from marmot.environment import (
    StateExhausted,
    ActionMissingKeys,
    RegistrationFailed,
    RegistrationConflict,
)


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


def test_bad_action_log(env):

    with pytest.raises(ActionMissingKeys):
        env._submit_log({"action": "TestAction"}, level="ACTION")


def test_env_state_shape(min_env, env):

    assert min_env.state.shape == (0,)

    assert env.state.shape == (24,)
    assert "temp" in env.state.dtype.names
    assert "workday" in env.state.dtype.names


def test_find_valid_constraints(env):

    valid1 = env._find_valid_constraints(temp=lt(10))
    assert len(valid1) == 1

    valid2 = env._find_valid_constraints(temp=10)
    assert len(valid2) == 0

    valid3 = env._find_valid_constraints(temp=lt(10), workday=true())
    assert len(valid3) == 2

    valid4 = env._find_valid_constraints(test=lt(10))
    assert len(valid4) == 0


def test_apply_constraints(env):

    # Temperature less than 100
    expected = np.concatenate(
        [np.array([True] * 12), np.array([False] * 6), np.array([True] * 6)]
    )

    output = env._apply_constraints(env.state, constraints={"temp": lt(100)})
    assert all(output == expected)

    # Working hours 7am - 8pm
    expected = np.concatenate(
        [np.array([False] * 6), np.array([True] * 14), np.array([False] * 4)]
    )

    output = env._apply_constraints(env.state, constraints={"workday": true()})
    assert all(output == expected)

    # Temperature less than 100, working hours 7am - 8pm
    expected = np.concatenate(
        [
            np.array([False] * 6),
            np.array([True] * 6),
            np.array([False] * 6),
            np.array([True] * 2),
            np.array([False] * 4),
        ]
    )

    output = env._apply_constraints(
        env.state, constraints={"temp": lt(100), "workday": true()}
    )
    assert all(output == expected)


def test_count_delay(env):
    arr1 = np.array([False, False, False, True, True])
    assert env._count_delays(arr1, 1) == [3, 1]
    assert env._count_delays(arr1, 2) == [3, 2]
    assert env._count_delays(arr1, 3) == None

    arr2 = np.array([True, True, False, False, True])
    assert env._count_delays(arr2, 1) == [1]
    assert env._count_delays(arr2, 2) == [2]
    assert env._count_delays(arr2, 3) == [2, 2, 1]
    assert env._count_delays(arr2, 4) == None

    arr3 = np.array([True, False, False, False, True, True, False, True])
    assert env._count_delays(arr3, 1) == [1]
    assert env._count_delays(arr3, 2) == [1, 3, 1]
    assert env._count_delays(arr3, 3) == [1, 3, 2]
    assert env._count_delays(arr3, 4) == [1, 3, 2, 1, 1]
    assert env._count_delays(arr3, 5) == None


def test_find_first_window(env):

    arr1 = np.array([False, False, False, True, True, True, False, False])
    assert env._find_first_window(arr1, 1) == 3
    assert env._find_first_window(arr1, 2) == 3
    assert env._find_first_window(arr1, 3) == 3
    assert env._find_first_window(arr1, 4) == None

    arr2 = np.array([True, True, False, True, True, True])
    assert env._find_first_window(arr2, 1) == 0
    assert env._find_first_window(arr2, 2) == 0
    assert env._find_first_window(arr2, 3) == 3
    assert env._find_first_window(arr2, 4) == None


def test_calculate_operational_delays(env, min_env):

    assert min_env.calculate_operational_delays(4, constraints={"temp": lt(100)}) == [4]

    assert env.calculate_operational_delays(4, constraints={"temp": lt(100)}) == [4]
    assert env.calculate_operational_delays(
        4, constraints={"temp": lt(100), "workday": true()}
    ) == [6, 4]
    assert env.calculate_operational_delays(
        8, constraints={"temp": lt(100), "workday": true()}
    ) == [6, 6, 6, 2]
    with pytest.raises(StateExhausted):
        env.calculate_operational_delays(19, constraints={"temp": lt(100)})


def test_find_operational_window(env, min_env):

    assert min_env.find_operational_window(4, constraints={"temp": lt(100)}) == 0

    assert env.find_operational_window(4, constraints={"temp": lt(100)}) == 0
    assert (
        env.find_operational_window(4, constraints={"temp": lt(100), "workday": true()})
        == 6
    )
    with pytest.raises(WindowNotFound):
        env.find_operational_window(8, constraints={"temp": lt(100), "workday": true()})
