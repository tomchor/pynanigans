
def get_coords(topology="PPN"):
    """
    Constructs the coords dict to be passed to xgcm.Grid
    Flat dimensions (F) are treated the same as Periodic ones (P)
    """
    x_per = dict(left="x_faa", center="x_caa")
    y_per = dict(left="y_afa", center="y_aca")
    z_per = dict(left="z_aaf", center="z_aac")

    x_nper = dict(outer="x_faa", center="x_caa")
    y_nper = dict(outer="y_afa", center="y_aca")
    z_nper = dict(outer="z_aaf", center="z_aac")

    per  = dict(x = x_per,  y = y_per,  z = z_per)
    nper = dict(x = x_nper, y = y_nper, z = z_nper)

    coords = { dim : per[dim] if top in "FP" else nper[dim] for dim, top in zip("xyz", topology) }

    return coords


def get_metrics(coords):
    """ 
    Constructs the metric dict based on `coords`.
    """
    metrics = {
        ("x",): [ "Δ" + coords["x"][key] for key in coords["x"].keys() ], # X distances
        ("y",): [ "Δ" + coords["y"][key] for key in coords["y"].keys() ], # Y distances
        ("z",): [ "Δ" + coords["z"][key] for key in coords["z"].keys() ], # Y distances
    }
    return metrics


def get_grid(ds, coords=None, metrics=None, topology="PPN", **kwargs):
    """ Gets xgcm grid for ds """
    import xgcm as xg

    if coords is None:
        coords = get_coords(topology)
    if metrics is None:
        metrics = get_metrics(coords)

    periodic = [ dim for (dim, top) in zip("xyz", topology) if top in "PF" ]
    return xg.Grid(ds, coords=coords, metrics=metrics,
                   periodic=periodic, **kwargs)
