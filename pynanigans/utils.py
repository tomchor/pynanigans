import xarray as xr

surjection = dict(xC='x',
                  xF='x',
                  yC='y',
                  yF='y',
                  zC='z',
                  zF='z',
                  )


def biject(darray, surjection=surjection, **kwargs):
    """
    Renames darray so that the dimension names actually correspond to the physical
    dimensions, instead of being the name of the grid meshes in Oceananigans.
    This makes calling functions easier as instead of calling `ds.u.plot(x='xF', y='zC')`, 
    you can call `ds.pnplot(x='x', y='z')`
    """
    da_dims = darray.dims
    bijection = { da_dim : dim for da_dim, dim in surjection.items() if da_dim in da_dims }
    return darray.rename(bijection)
xr.DataArray.biject = biject


def pnmean(darray, *args, surjection=surjection, **kwargs):
    """
    Bijects darray to change the names of the dimensions before calling
    xarray's mean() function
    """
    return biject(darray, surjection=surjection).mean(*args, **kwargs)
xr.DataArray.pnmean = pnmean


def regular_indef_integrate(f, dim):
    """
    Computes the indefinite integral (or antiderivative) of f over the dimension f
    when f is equaly spaced in dim.
    """
    Δt = f[dim].diff(dim).mean()
    return f.cumsum(dim) * Δt


def normalize_time_by(ds, seconds=1, new_units="seconds"):
    """ 
    Converts the time dimension (a timedelta[ns] object by default) into a np.float64
    object while normalizing it by number of seconds `seconds`.
    """
    import numpy as np
    if ds.time.dtype == '<m8[ns]': # timedelta[ns]
        ds = ds.assign_coords(time = ds.time.astype(np.float64)/1e9/seconds) # From timedelta[ns] to seconds
    elif ds.time.dtype == 'float64':
        ds = ds.assign_coords(time = ds.time.astype(np.float64)/seconds) # From timedelta[ns] to seconds
    else:
        raise(TypeError("Unknown type for time"))
    ds.time.attrs = dict(units=label)
    return ds


