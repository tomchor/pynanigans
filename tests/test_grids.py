import pytest
import xarray as xr
import numpy as np
from pynanigans.grids import get_coords, get_metrics, get_grid

def test_get_coords():
    # Test periodic coordinates
    coords = get_coords(topology="PPP")
    assert "x" in coords
    assert "y" in coords
    assert "z" in coords
    assert coords["x"]["left"] == "xF"
    assert coords["x"]["center"] == "xC"

    # Test non-periodic coordinates
    coords = get_coords(topology="NNN")
    assert coords["x"]["outer"] == "xF"
    assert coords["x"]["center"] == "xC"

def test_get_metrics():
    # Create a test dataset
    data = np.random.rand(10, 10, 10)
    dims = ['xC', 'yC', 'zC']
    coords = {
        'xC': np.linspace(0, 1, 10),
        'yC': np.linspace(0, 1, 10),
        'zC': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test metrics
    metrics = get_metrics(ds)
    assert ('x',) in metrics
    assert ('y',) in metrics
    assert ('z',) in metrics
    assert "ΔxC" in metrics[('x',)]
    assert "ΔxF" in metrics[('x',)]

def test_get_grid():
    # Create a test dataset
    data = np.random.rand(10, 10, 10)
    dims = ['xC', 'yC', 'zC']
    coords = {
        'xC': np.linspace(0, 1, 10),
        'yC': np.linspace(0, 1, 10),
        'zC': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test grid creation
    grid = get_grid(ds, topology="PPP")
    assert grid is not None
    assert hasattr(grid, 'coords')
    assert hasattr(grid, 'metrics')