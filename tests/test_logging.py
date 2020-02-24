"""Tests for `marmot.Environment` logging functionality."""

__author__ = "Jake Nunemaker"
__copyright__ = "Copyright 2019, Jake Nunemaker"
__email__ = "jake.d.nunemaker@gmail.com"
__status__ = "Development"


import _simpy


def test_single_agent_logging(env, ExampleAgent):

    agent = ExampleAgent()
    env.register(agent)

    agent.pause(10)
    env.run()

    assert len(env.logs) == 1
    assert env.logs[-1]["time"] == 10

    agent.pause_then_perform(5, 10)
    env.run()

    assert len(env.actions) == 3
    assert len(env.logs) == 4
    assert env.logs[-1]["time"] == 25


def test_multiple_agent_logging(env, ExampleAgent):

    agent1 = ExampleAgent("Agent 1")
    agent2 = ExampleAgent("Agent 2")
    env.register(agent1)
    env.register(agent2)

    event = _simpy.Event(env)

    agent1.wait_for_event(event, 25)
    agent2.trigger_event_after(event, 25)

    env.run()

    assert len(env.actions) == 3
    assert len(env.logs) == 5
    assert env.logs[-1]["time"] == 50

    agent1_actions = [a for a in env.actions if a["agent"] == "Agent 1"]
    agent2_actions = [a for a in env.actions if a["agent"] == "Agent 2"]

    assert agent1_actions[0]["time"] == 25
    assert agent1_actions[0]["action"] == "WaitForEvent"
    assert agent1_actions[0]["status"] == "DoneWaiting"

    assert agent2_actions[0]["time"] == 25
    assert agent2_actions[0]["action"] == "Pause"

    assert agent1_actions[1]["time"] == 50
    assert agent1_actions[1]["action"] == "Perform"
    assert agent1_actions[1]["status"] == "Successful"
