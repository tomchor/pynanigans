import pytest
import xarray as xr
import numpy as np
from pynanigans.pnplot import pnplot, _imshow, _pcolormesh, _contour, _contourf

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
    plot = _imshow(ds.u, x='x_caa', y='y_aca')
    assert plot is not None

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
    plot = _pcolormesh(ds.u, x='x_caa', y='y_aca')
    assert plot is not None

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
    plot = _contour(ds.u, x='x_caa', y='y_aca')
    assert plot is not None

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
    plot = _contourf(ds.u, x='x_caa', y='y_aca')
    assert plot is not None