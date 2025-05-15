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
    assert coords["x"]["left"] == "x_faa"
    assert coords["x"]["center"] == "x_caa"
    
    # Test non-periodic coordinates
    coords = get_coords(topology="NNN")
    assert coords["x"]["outer"] == "x_faa"
    assert coords["x"]["center"] == "x_caa"

def test_get_metrics():
    # Create a test dataset
    data = np.random.rand(10, 10, 10)
    dims = ['x_caa', 'y_aca', 'z_aac']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10),
        'z_aac': np.linspace(0, 1, 10)
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
    assert "Δx_caa" in metrics[('x',)]
    assert "Δx_faa" in metrics[('x',)]
