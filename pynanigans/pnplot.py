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
xr.DataArray.pnplot.imshow = xr.DataArray.pnimshow
