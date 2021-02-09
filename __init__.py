__version__ = "0.0.0"

def get_coords(ds, topology="PPN",):
    """ Constructions the coords dict for ds """
    per = dict(left='xF', center='xC')
    nper = dict(outer='xF', center='xC')
    per = { dim : dict(left=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    nper = { dim : dict(outer=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    coords = { dim : per[dim] if top=="P" else nper[dim] for dim, top in zip("xyz", topology) }
    
    return coords


def get_metrics(ds):
    """ 
    Constructs the metric dict for ds.
    (Not sure if the metrics are correct at the boundary points
    """
    if "Δx" not in ds.variables: 
        ds["Δx"] = ds.xC.diff('xC').mean().item()
    if "Δy" not in ds.variables: 
        ds["Δy"] = ds.yC.diff('yC').mean().item()
    if "Δz" not in ds.variables: 
        ds["Δz"] = ds.zC.diff('zC').mean().item()

    metrics = {
        ('x',): ['Δx'], # X distances
        ('y',): ['Δy'], # Y distances
        ('z',): ['Δz'], # Z distances
    }

    return metrics


def get_grid(ds, coords=None, metrics=None, topology="PPN", **kwargs):
    """ Gets xgcm grid for ds """
    import xgcm as xg

    if coords is None:
        coords = get_coords(ds, topology=topology)
    if metrics is None:
        metrics = get_metrics(ds)
    return xg.Grid(ds, coords=coords, metrics=metrics, **kwargs)


