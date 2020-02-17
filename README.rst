
Marmot
======

Marmot is an extension of `SimPy <https://simpy.readthedocs.io/en/latest/>`_
that makes it easier to build agent-based process models. Marmot allows a user
to model the actions of discrete agents acting within an environment.

:Version: 0.2.4
:Authors: `Jake Nunemaker <https://www.linkedin.com/in/jake-nunemaker/>`_
:Documentation: Coming soon!

Installation
------------

``pip install marmot-agents``

Getting Started
---------------

.. code-block:: python

   from marmot import Environment, Agent

   # An agent must be created and registered to an environment
   env = Environment()
   agent = Agent("Test Agent")
   env.register(agent)

   # The registered agent can now be scheduled to perform tasks
   agent.task("Run", 10)  # The agent is scheduled to run for 10 units of time

   # The simulation must be ran
   env.run()
   print(env.now)
   >>> 10

   # Logs of all tasks are kept
   env.logs
   >>> [{"agent": "Test Agent", "action": "Run", "duration": 10, "time": 10}]
