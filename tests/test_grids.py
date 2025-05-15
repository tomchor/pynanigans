import pytest
import xarray as xr
import numpy as np
from pynanigans.grids import get_coords, get_metrics, get_grid

def test_get_coords():
    # Test periodic coordinates
    coords = get_coords(None, topology="PPP")
    assert "x" in coords
    assert "y" in coords
    assert "z" in coords
    assert coords["x"]["left"] == "xF"
    assert coords["x"]["center"] == "xC"

    # Test non-periodic coordinates
    coords = get_coords(None, topology="NNN")
    assert coords["x"]["outer"] == "xF"
    assert coords["x"]["center"] == "xC"
