import pytest
import xarray as xr
import numpy as np
from pynanigans.utils import biject, normalize_time_by, downsample, pnchunk

def test_biject():
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

    # Test bijection
    result = biject(ds.u)
    assert 'x' in result.dims
    assert 'y' in result.dims
    assert 'z' in result.dims
    assert 'x_caa' not in result.dims
    assert 'y_aca' not in result.dims
    assert 'z_aac' not in result.dims

def test_normalize_time_by():
    # Create a test dataset with time
    data = np.random.rand(10)
    time = np.array([np.timedelta64(i, 'ns') for i in range(10)])
    ds = xr.Dataset(
        data_vars={'u': ('time', data)},
        coords={'time': time}
    )

    # Test normalization
    result = normalize_time_by(ds.u, seconds=1)
    assert result.time.dtype == 'float64'
    assert result.time.attrs['units'] == 'seconds'

def test_downsample():
    # Create a test dataset
    data = np.random.rand(100, 100)
    dims = ['x_caa', 'y_aca']
    coords = {
        'x_caa': np.linspace(0, 1, 100),
        'y_aca': np.linspace(0, 1, 100)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test downsampling
    result = downsample(ds.u, x_caa=50, y_aca=50)
    assert len(result.x_caa) == 50
    assert len(result.y_aca) == 50

def test_pnchunk():
    # Create a test dataset with time
    data = np.random.rand(100, 10, 10, 10)
    time = np.array([np.timedelta64(i, 'ns') for i in range(100)])
    dims = ['time', 'x_caa', 'y_aca', 'z_aac']
    coords = {
        'time': time,
        'x_caa': np.linspace(0, 1, 10),
        'y_aca': np.linspace(0, 1, 10),
        'z_aac': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test chunking
    result = pnchunk(ds.u, maxsize_4d=1000)
    result = pnchunk(ds, maxsize_4d=1000)
    assert any(result.chunks)
