import pytest
import xarray as xr
import numpy as np
from pynanigans import pnplot

def test_pnplot():
    # Create a test dataset
    data = np.random.rand(10, 10)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test plotting
    plot = pnplot(ds.u, x='x_caa', y='y_aca')
    assert plot is not None

    # Test error case - invalid dimension
    with pytest.raises(ValueError):
        pnplot(ds.u, x='invalid_dim', y='y_aca')

def test_imshow():
    # Create a test dataset
    data = np.random.rand(10, 10)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test imshow
    plot = ds.u.pnimshow(x='x_caa', y='y_aca')
    assert plot is not None

    # Test error case - invalid dimension
    with pytest.raises(ValueError):
        ds.u.pnimshow(x='invalid_dim', y='y_aca')

def test_pcolormesh():
    # Create a test dataset
    data = np.random.rand(10, 10)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test pcolormesh
    plot = ds.u.pnpcolormesh(x='x_caa', y='y_aca')
    assert plot is not None

    # Test error case - invalid dimension
    with pytest.raises(ValueError):
        ds.u.pnpcolormesh(x='invalid_dim', y='y_aca')

def test_contour():
    # Create a test dataset
    data = np.random.rand(10, 10)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test contour
    plot = ds.u.pncontour(x='x_caa', y='y_aca')
    assert plot is not None

    # Test error case - invalid dimension
    with pytest.raises(ValueError):
        ds.u.pncontour(x='invalid_dim', y='y_aca')

def test_contourf():
    # Create a test dataset
    data = np.random.rand(10, 10)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test contourf
    plot = ds.u.pncontourf(x='x_caa', y='y_aca')
    assert plot is not None

    # Test error case - invalid dimension
    with pytest.raises(ValueError):
        ds.u.pncontourf(x='invalid_dim', y='y_aca')