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

