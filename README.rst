trips-web
=========

Installation: `pip install trips-web`.

.. code-block:: bash

  trips-web -h
  trips-web "This is a test sentence." > parse.xml


config.json
===========

If you wish to define a configuration file in json, just set each parameter in a json dict, replacing any dashes (-) with underscores (_).

.. code-block:: bash

  trips-web [commands] --dump

returns a json document with the configuration instead of the parse.
