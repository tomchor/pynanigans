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

def test_read_uvw_nc():
    # Get the path to the test data file
    test_data_path = "uvw.nc"

    # Read the netCDF file
    grid, ds = xr.open_simulation(test_data_path)

    # Basic dataset structure checks
    assert "u" in ds
    assert "v" in ds
    assert "w" in ds

    # Check dimensions
    assert "x_caa" in ds.dims
    assert "y_aca" in ds.dims
    assert "z_aac" in ds.dims

    # Check coordinate variables
    assert "x_caa" in ds.coords
    assert "y_aca" in ds.coords
    assert "z_aac" in ds.coords

    # Check data types and shapes
    assert ds.u.dtype in [np.float32, np.float64]
    assert ds.v.dtype in [np.float32, np.float64]
    assert ds.w.dtype in [np.float32, np.float64]

    # Check that all variables have the same dimensions
    assert ds.u.dims == ds.v.dims == ds.w.dims
    
    # Close the dataset
    ds.close()
