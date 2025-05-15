import tomli
from pathlib import Path

# Read version from pyproject.toml
with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    __version__ = pyproject["project"]["version"]

from .grids import get_metrics, get_coords, get_grid
from .utils import *
from . import pnplot
from . import utils

