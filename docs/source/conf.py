"""Sphinx configuration for ECabc."""

from __future__ import annotations

import sys
from importlib.metadata import version as pkg_version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

project = "ECabc"
copyright = "2018-2026, Sanskriti Sharma, Hernan Gelaf-Romer, Travis Kessler"
author = "Sanskriti Sharma, Hernan Gelaf-Romer, Travis Kessler"
release = pkg_version("ecabc")
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "furo"
html_static_path = ["_static"]
html_title = f"{project} {release}"

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_use_param = True
napoleon_use_rtype = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
