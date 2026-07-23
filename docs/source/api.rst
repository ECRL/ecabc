API reference
=============

Primary entry point
-------------------

:class:`ecabc.ABC` is the supported workflow for application code. See
:doc:`stability` for the frozen contract.

.. autoclass:: ecabc.ABC
   :members:
   :undoc-members:
   :show-inheritance:

Secondary exports
-----------------

:class:`ecabc.Bee`, :class:`ecabc.Parameter`, and ``ecabc.utils`` remain part of
the frozen ``3.x`` surface. Prefer the ``ABC`` workflow for new code; these
types are useful for tests, extensions, and advanced inspection.

.. autoclass:: ecabc.Bee
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ecabc.Parameter
   :members:
   :undoc-members:
   :show-inheritance:

Package version
---------------

.. autodata:: ecabc.__version__

Utilities
---------

Import helpers as ``import ecabc.utils``. Public functions:

* ``apply_mutation``
* ``call_obj_fn``
* ``choose_bee``
* ``determine_best_bee``

.. automodule:: ecabc.utils
   :members:
   :undoc-members:
   :show-inheritance:
