import xarray as xr
from .utils import surjection, biject


def pnplot(darray, surjection=surjection, **kwargs):
    """
    Bijects darray to rename the dimensions before calling plot().
    This makes plot easier as, instead of calling, `ds.u.plot(x='xF', y='zC')`,
    you can call `ds.pnplot(x='x', y='z')`
    """
    return biject(darray, surjection=surjection).plot(**kwargs)
xr.DataArray.pnplot = pnplot

def _imshow(darray, surjection=surjection, **kwargs):
    """ Wrapper around DataArray.plot.imshow """
    return biject(darray, surjection=surjection).plot.imshow(**kwargs)
xr.DataArray.pnimshow = _imshow

def _pcolormesh(darray, surjection=surjection, **kwargs):
    """ Wrapper around DataArray.plot.pcolormesh """
    return biject(darray, surjection=surjection).plot.pcolormesh(**kwargs)
xr.DataArray.pnpcolormesh = _pcolormesh

def _contour(darray, surjection=surjection, **kwargs):
    """ Wrapper around DataArray.plot.contour """
    return biject(darray, surjection=surjection).plot.contour(**kwargs)
xr.DataArray.pncontour = _contour

def _contourf(darray, surjection=surjection, **kwargs):
    """ Wrapper around DataArray.plot.contourf """
    return biject(darray, surjection=surjection).plot.contourf(**kwargs)
xr.DataArray.pncontourf = _contourf
