from importlib.metadata import PackageNotFoundError, version

from ecabc.abc import ABC
from ecabc.bee import Bee
from ecabc.parameter import Parameter

from . import utils as utils

__all__ = ["ABC", "Bee", "Parameter", "__version__", "utils"]


def _resolve_version() -> str:
    try:
        return version("ecabc")
    except PackageNotFoundError:
        return "0.0.0+unknown"


__version__ = _resolve_version()
