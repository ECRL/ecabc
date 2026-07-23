Installation
============

Requires **Python 3.10** or newer (``requires-python = ">=3.10"``). ECabc has no
runtime third-party dependencies (stdlib only). A virtual environment is
recommended.

Install from PyPI
-----------------

.. code-block:: bash

   pip install ecabc

Upgrade
-------

.. code-block:: bash

   pip install --upgrade ecabc

Install from source
-------------------

Clone or download the repository, then from the repository root:

.. code-block:: bash

   pip install .

Development extras
------------------

Contributor tooling and documentation builds use optional extras:

.. code-block:: bash

   pip install -e ".[dev]"
   pip install -e ".[docs]"

``[dev]`` includes pytest, coverage, ruff, mypy, pre-commit, and build.
``[docs]`` includes Sphinx, Furo, and related extensions.

Build the HTML docs locally
---------------------------

.. code-block:: bash

   pip install -e ".[docs]"
   sphinx-build -W -b html docs/source docs/_build/html
