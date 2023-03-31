g.. PySWAPI documentation master file, created by
   sphinx-quickstart on Mon Mar 27 22:14:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PySWAPI's documentation!
===================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


What is PySWAPI?
================
PySWAPI is a Python library for interacting with the SensorWebAPI (SWAPI) and later, the ConnectedSystemsAPI
as support for that is improved within OSH Core.

At the core, PySWAPI depends on a small package called 'oshdatacore' which provides a simplified representation of
OGC's SWE Common Data Model V2.0.

.. note:: OSHDataCore is not yet published on PyPI, so it needs to be installed manually.
    For now, you can install it by cloning the repository from GitHub and running:

    .. code-block:: bash

        pip install oshdatacore@git+https://github.com/ChainReaction31/py_osh_data_core.git


PySWAPI Systems
===============

The System module is the heart and soul of the PySWAPI library. Every other part of the library will, at some point,
have to interact with a System. It is as representation of a single OSH system that allows access to Datastreams
and their Observations, FeaturesOfInterest, ControlStreams and their Commands.

.. automodule:: pyswapi.system
   :members:
   :undoc-members:
   :show-inheritance:

PySWAPI Datastreams and Observations
====================================

The Datastreams and Observations module is the main reason you likely are interested in PySWAPI. It provides
the objects and methods necessary to actually send data to an OSH Node.

.. automodule:: pyswapi.datastreams_and_observations
   :members:
   :undoc-members:
   :show-inheritance:

PySWAPI Control Streams and Commands
====================================

The Control Streams and Commands module is responsible for creating control interfaces and interacting with them
through commands and status updates.

.. automodule:: pyswapi.control_streams_and_commands
   :members:
   :undoc-members:
   :show-inheritance:

PySWAPI Constants
=================

The Constants module is a collection of constant values that make appearances throughout the library.
It's unlikely that you'll be using them too often, but they're there if you need them.

.. automodule:: pyswapi.constants
   :members:
   :undoc-members:
   :show-inheritance: