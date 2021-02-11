import xarray as xr

surjection = dict(xC='x',
                  xF='x',
                  yC='y',
                  yF='y',
                  zC='z',
                  zF='z',
                  )


def pnplot(darray, surjection=surjection, **kwargs):
    """
    Renames darray so that the dimension names actually correspond to the physical
    dimensinos, instead of being the name of the grid meshes in Oceananigans.
    This makes plot easier as, instead of calling, `ds.u.plot(x='xC', y='zF')`, 
    you can call `ds.pnplot(x='x', y='z')`
    """
    da_dims = darray.dims
    bijection = { da_dim : dim for da_dim, dim in surjection.items() if da_dim in da_dims }
    return darray.rename(bijection).plot(**kwargs)

xr.DataArray.pnplot = pnplot
