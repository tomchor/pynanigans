import pytest
import xarray as xr
import numpy as np
from pynanigans.utils import open_simulation
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
    metrics = get_metrics(get_coords("PPP"))
    assert ('x',) in metrics
    assert ('y',) in metrics
    assert ('z',) in metrics
    assert "Δx_caa" in metrics[('x',)]
    assert "Δx_faa" in metrics[('x',)]

def test_read_uvw_nc():
    # Get the path to the test data file
    test_data_path = "uvw.nc"

    # Read the netCDF file
    grid, ds = open_simulation(test_data_path, topology="PPN")

    # Basic dataset structure checks
    assert "u" in ds
    assert "v" in ds
    assert "w" in ds

    assert "Δx_caa" in ds
    assert "Δx_faa" in ds
    assert "Δy_aca" in ds
    assert "Δy_afa" in ds
    assert "Δz_aac" in ds
    assert "Δz_aaf" in ds

    # Check dimensions
    assert "time" in ds.dims
    assert "x_caa" in ds.dims
    assert "x_faa" in ds.dims
    assert "y_aca" in ds.dims
    assert "y_afa" in ds.dims
    assert "z_aac" in ds.dims
    assert "z_aaf" in ds.dims

    # Check coordinate variables
    assert "time" in ds.coords
    assert "x_caa" in ds.coords
    assert "x_faa" in ds.coords
    assert "y_aca" in ds.coords
    assert "y_afa" in ds.coords
    assert "z_aac" in ds.coords
    assert "z_aaf" in ds.coords

    # Check data types and shapes
    assert ds.u.dtype in [np.float32, np.float64]
    assert ds.v.dtype in [np.float32, np.float64]
    assert ds.w.dtype in [np.float32, np.float64]

    # Check that sizes are right after operations
    assert grid.diff(ds.u, "x").shape[1] == len(ds.x_faa)
    assert grid.diff(ds.v, "y").shape[2] == len(ds.y_afa)
    assert grid.diff(ds.w, "z").shape[3] == len(ds.z_aac)

    assert grid.interp(ds.u, "x").shape[1] == len(ds.x_faa)
    assert grid.interp(ds.v, "y").shape[2] == len(ds.y_afa)
    assert grid.interp(ds.w, "z").shape[3] == len(ds.z_aac)

    assert "z_aaf" in grid.interp(ds.u, "z").coords
    assert "z_aaf" in grid.interp(ds.v, "z").coords
    assert "x_faa" in grid.interp(ds.w, "x").coords

    # Close the dataset
    ds.close()
