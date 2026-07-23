API stability policy
====================

This page is the user-facing stability contract for **ecabc**. A copy also lives
at the repository root as ``API_STABILITY.md`` for contributors who browse the
source tree without building the docs.

ECabc implements the Artificial Bee Colony (ABC) metaheuristic for tuning
parameters of user-supplied objective functions. Background literature:

* Karaboğa D. Artificial bee colony algorithm. *Scholarpedia*, 5(3):6915, 2010.
  https://www.scholarpedia.org/article/Artificial_bee_colony_algorithm
* Package paper (JOSS): DOI `10.21105/joss.01420`
  https://doi.org/10.21105/joss.01420

Frozen public surface
---------------------

The following imports are the supported surface and must remain drop-in
compatible within the ``3.0.x`` / ``3.1.x`` compatibility series:

.. code-block:: python

   from ecabc import ABC, Bee, Parameter
   import ecabc.utils
   from ecabc import __version__

:class:`ecabc.ABC` is the **primary** documented entry point. Parameter
**names** and **defaults** for its public methods are frozen. Additive optional
keyword arguments may be introduced when they do not change existing call sites.
Renaming methods, making new arguments required, changing primary return
container types, or changing documented exception types for existing failure
modes requires an explicit, versioned compatibility decision.

Primary workflow (``ABC``)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Signatures and defaults to preserve (keyword names and defaults must remain
compatible):

.. code-block:: python

   ABC(
       num_employers: int,
       objective_fn,                 # callable
       obj_fn_args: dict = {},
       num_processes: int = 1,
   )

   abc.add_param(
       min_val,                      # int or float
       max_val,                      # same type as min_val
       restrict: bool = True,
       name: str | None = None,
   )

   abc.initialize()
   abc.search()

   abc.best_fitness                  # float
   abc.best_ret_val                  # numeric or None
   abc.best_params                   # dict
   abc.average_fitness               # float or None
   abc.average_ret_val               # float or None

Objective-function contract
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Rule
     - Contract
   * - Input
     - A ``list`` of parameter values (``int`` and/or ``float``)
   * - Output
     - Numeric objective value
   * - Sense
     - Lower return values are better
   * - Extra args
     - Via ``obj_fn_args`` kwargs passed through to the objective

Exception and warning contracts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Condition
     - Type
   * - Non-callable objective
     - ``ReferenceError``
   * - ``add_param`` after ``initialize``
     - ``RuntimeError``
   * - ``search`` before ``initialize``
     - ``RuntimeError``
   * - Second ``initialize``
     - ``RuntimeWarning``
   * - Parameter min/max type mismatch
     - ``ValueError``

Behavioral invariants
~~~~~~~~~~~~~~~~~~~~~

The following must not change without a major-version plan:

1. After ``initialize``, colony size is ``2 × num_employers`` (employers + onlookers).
2. Stay limit is ``num_employers × num_parameters``.
3. Default keys in ``best_params`` are ``P0``, ``P1``, … when ``name`` is omitted.
4. Fitness transform follows ``Bee.calc_fitness``: ``1/(1+ofv)`` if ``ofv >= 0``,
   else ``1 + abs(ofv)``.

Secondary exports
~~~~~~~~~~~~~~~~~

:class:`ecabc.Bee`, :class:`ecabc.Parameter`, and ``ecabc.utils``
(``apply_mutation``, ``call_obj_fn``, ``choose_bee``, ``determine_best_bee``)
remain importable. They are **secondary** relative to the ``ABC`` workflow but
are part of the frozen ``3.x`` surface and must not be removed without a
major-version plan. Prefer :class:`ecabc.ABC` for new application code.

Version export
~~~~~~~~~~~~~~

``ecabc.__version__`` is part of the public surface. Callers may rely on it
resolving to the installed package version string.

Versioning
----------

1. **Patch (``3.0.x``):** bugfixes, tooling, packaging, documentation, and
   internal hardening that preserve the frozen API. The API-stable modernization
   program ships as **``3.0.2``**.
2. **Minor (``3.1.0`` and later):** reserved for future additive, still
   API-compatible work after ``3.0.2``.
3. **Major (``4.0.0`` or higher):** only after an explicit stability or migration
   plan (for example an intentional algorithm-semantics change or API redesign).

Runtime dependencies
--------------------

The default install is **stdlib-only** (no required third-party runtime
packages). Optional developer or documentation extras may exist for contributors
and do not change the runtime contract for ``pip install ecabc``.
