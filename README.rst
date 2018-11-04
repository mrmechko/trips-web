trips-web
=========

Simple command-line `api <http://trips.ihmc.us/parser/api.html>`_ for the `TRIPS web parser <http://trips.ihmc.us/parser/cgi/parse>`_

Installation:

.. code-block:: bash

  git clone http://github.com/mrmechko/trips-web
  cd trips-web
  pip install .

.. code-block:: bash

  trips-web -h
  trips-web "This is a test sentence." > parse.json


config.json
===========

If you wish to define a configuration file in json, just set each parameter in a json dict, replacing any dashes (-) with underscores (_).

.. code-block:: bash

  trips-web [commands] --dump

returns a json document with the configuration instead of the parse.
