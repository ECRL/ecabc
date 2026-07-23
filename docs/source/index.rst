ECabc documentation
===================

**ECabc** is an open-source Python package that tunes parameters of
user-supplied objective (fitness) functions using the Artificial Bee Colony
(ABC) algorithm. The runtime install is stdlib-only. The primary public entry
point is :class:`ecabc.ABC`.

Background
----------

* Karaboğa D. Artificial bee colony algorithm. *Scholarpedia*, 5(3):6915, 2010.
  https://www.scholarpedia.org/article/Artificial_bee_colony_algorithm
* Sharma, S., Gelaf-Romer, H., Kessler, T., & Mack, J. H. (2019). ECabc
  (JOSS). DOI `10.21105/joss.01420` https://doi.org/10.21105/joss.01420

The colony uses employer, onlooker, and scout roles to explore a bounded
parameter space. Lower objective values are treated as better.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   stability
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
