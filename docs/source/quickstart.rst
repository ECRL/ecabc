Quickstart
==========

Define an objective function that accepts a ``list`` of parameter values and
returns a numeric score (**lower is better**):

.. code-block:: python

   def minimize_integers(integers):
       return sum(integers)

Create a colony, add parameters, initialize, and search:

.. code-block:: python

   from ecabc import ABC

   abc = ABC(10, minimize_integers)
   abc.add_param(0, 10, name="Int_1")
   abc.add_param(0, 10, name="Int_2")
   abc.add_param(0, 10, name="Int_3")
   abc.initialize()
   for _ in range(50):
       abc.search()

   print(abc.best_params)
   print(abc.best_ret_val)

Notes
-----

* By default, mutated parameter values stay within ``[min_val, max_val]``. Pass
  ``restrict=False`` to :meth:`ecabc.ABC.add_param` to allow out-of-bounds
  mutations.
* Optional non-tunable kwargs can be forwarded with ``obj_fn_args`` on
  :class:`ecabc.ABC`.
* Parallel objective evaluation uses ``num_processes`` (stdlib
  ``multiprocessing``).

Next steps
----------

* :doc:`stability` — frozen imports, exceptions, and versioning
* :doc:`api` — autodoc for :class:`ecabc.ABC` and secondary exports
* Repository ``README.md`` — longer tutorial-style walkthrough
