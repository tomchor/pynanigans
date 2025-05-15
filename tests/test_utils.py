import pytest
import xarray as xr
import numpy as np
from pynanigans.utils import biject, normalize_time_by, downsample, pnchunk

def test_biject():
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

    # Test bijection
    result = biject(ds.u)
    assert 'x' in result.dims
    assert 'y' in result.dims
    assert 'z' in result.dims
    assert 'xC' not in result.dims
    assert 'yC' not in result.dims
    assert 'zC' not in result.dims

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
    dims = ['xC', 'yC']
    coords = {
        'xC': np.linspace(0, 1, 100),
        'yC': np.linspace(0, 1, 100)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test downsampling
    result = downsample(ds.u, xC=50, yC=50)
    assert len(result.xC) == 50
    assert len(result.yC) == 50

def test_pnchunk():
    # Create a test dataset with time
    data = np.random.rand(100, 10, 10, 10)
    time = np.array([np.timedelta64(i, 'ns') for i in range(100)])
    dims = ['time', 'xC', 'yC', 'zC']
    coords = {
        'time': time,
        'xC': np.linspace(0, 1, 10),
        'yC': np.linspace(0, 1, 10),
        'zC': np.linspace(0, 1, 10)
    }
    ds = xr.Dataset(
        data_vars={'u': (dims, data)},
        coords=coords
    )

    # Test chunking
    result = pnchunk(ds.u, maxsize_4d=1000)
    assert 'chunks' in result.encoding