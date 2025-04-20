import xarray as xr
from .grids import get_grid

surjection = dict(x_caa='x',
                  xF='x',
                  y_aca='y',
                  yF='y',
                  z_aac='z',
                  zF='z',
                  )


def biject(darray, *args, surjection=surjection):
    """
    Renames darray so that the dimension names actually correspond to the physical
    dimensions, instead of being the name of the grid meshes in Oceananigans.
    If `*args` is provided, only those dimensions will be renamed. If not, `x`, `y` 
    and `z` will be automatically renamed.

    This makes calling functions easier as instead of calling `darray.u.plot(x='xF', y='z_aac')`, 
    you can call `darray.pnplot(x='x', y='z')`
    """
    da_dims = darray.dims
    if args:
        bijection = { da_dim : dim for da_dim, dim in surjection.items() if (da_dim in da_dims and dim in args) }
    else:
        bijection = { da_dim : dim for da_dim, dim in surjection.items() if da_dim in da_dims }
    return darray.rename(bijection)
xr.DataArray.biject = biject


def regular_indef_integrate(f, dim):
    """
    Computes the indefinite integral (or antiderivative) of f over the dimension f
    when f is equaly spaced in dim.
    """
    Δt = f[dim].diff(dim).mean()
    return f.cumsum(dim) * Δt


def normalize_time_by(darray, seconds=1, new_units="seconds"):
    """ 
    Converts the time dimension (a timedelta[ns] object by default) into a np.float64
    object while normalizing it by number of seconds `seconds`.
    """
    import numpy as np
    if darray.time.dtype == '<m8[ns]': # timedelta[ns]
        darray = darray.assign_coords(time = darray.time.astype(np.float64)/1e9/seconds) # From timedelta[ns] to seconds
    elif darray.time.dtype == 'float64':
        darray = darray.assign_coords(time = darray.time.astype(np.float64)/seconds) # From timedelta[ns] to seconds
    else:
        raise(TypeError("Unknown type for time"))
    darray.time.attrs = dict(units=new_units)
    return darray



def downsample(darray, round_func=round, **dim_limits):
    """
    Downsamples `darray` based on dimensions given in dim_limits

    dim_limits should be of the form:
        dim_limits = dict(y_aca=1000, zF=2048)
    """
    for dim, dim_limit in dim_limits.items():
        dim_length = len(darray[dim])
        stride = int(round_func(dim_length / dim_limit))
        down = {dim : slice(None, None, stride)}
        darray = darray.isel(**down)
    return darray



def pnchunk(darray, maxsize_4d=1000**2, sample_var="u", round_func=round, **kwargs):
    """ Chunk `darray` in time while keeping each chunk's size roughly 
    around `maxsize_4d`. The default `maxsize_4d=1000**2` comes from
    xarray's rule of thumb for chunking:
    http://xarray.pydata.org/en/stable/dask.html#chunking-and-performance
    """
    chunk_number = darray[sample_var].size / maxsize_4d
    chunk_size = int(round_func(len(darray[sample_var].time) / chunk_number))
    return darray.chunk(dict(time=chunk_size))
xr.DataArray.pnchunk = pnchunk
xr.Dataset.pnchunk = pnchunk


funcnames_nonreduc = ["sel", "isel", "diff", "differentiate"]
for funcname in funcnames_nonreduc:
    funcdef = f'''
def pn{funcname}(darray, surjection=surjection, **kwargs):
    """
    Bijects darray to change the names of the dimensions before calling
    xarray's `{funcname}()` function
    """
    dims = [ dim for dim in kwargs.keys() if dim in surjection.values() ]
    return biject(darray, *dims, surjection=surjection).{funcname}(**kwargs)
xr.DataArray.pn{funcname} = pn{funcname}
xr.Dataset.pn{funcname} = pn{funcname}'''
    exec(funcdef)


funcnames_reduc = ["sum", "integrate", "mean", "std", "var", "max", "min", "median"]
for funcname in funcnames_reduc:
    funcdef = f'''
def pn{funcname}(darray, dim=None, surjection=surjection, **kwargs):
    """
    Bijects darray to change the names of the dimensions before calling
    xarray's `{funcname}()` function
    """
    if dim is None: # biject() receives a list of dims; funcname() receives iterable
        bj_dims = ()
    elif isinstance(dim, tuple) or isinstance(dim, list):
        bj_dims = dim
    else:
        bj_dims = [dim]
    return biject(darray, *bj_dims, surjection=surjection).{funcname}(dim, **kwargs)
xr.DataArray.pn{funcname} = pn{funcname}
xr.Dataset.pn{funcname} = pn{funcname}'''
    exec(funcdef)


def open_simulation(fname, 
                    grid_kwargs=dict(),
                    load=False,
                    squeeze=True,
                    verbose=False,
                    unique=True,
                    topology="PPN", **kwargs):
    """
    Opens a NetCDF file, returning an xarray.Dataset and a xgcm.Grid.

    `kwargs` are passed to `xarray.open_dataset()` and `grid_kwargs` are passed to `pynanigans.get_grid()`.
    """
    
    #++++ Open dataset and create grid before squeezing
    if load:
        ds = xr.load_dataset(fname, **kwargs)
    else:
        ds = xr.open_dataset(fname, **kwargs)
    grid_ds = get_grid(ds, topology=topology, **grid_kwargs)
    #----

    #++++ Squeeze?
    if squeeze: ds = ds.squeeze()
    #----

    #++++ Returning only unique times. Useful if simulation was restarted and there's overlap in time
    if unique:
        import numpy as np
        _, index = np.unique(ds['time'], return_index=True)
        if verbose and (len(index)!=len(ds.time)): print("Cleaning non-unique indices")
        ds = ds.isel(time=index)
    #----

    return grid_ds, ds

