
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


def get_metrics(ds, topology="PPN"):
    """ 
    Constructs the metric dict for `ds`.
    (Not sure if the metrics are correct at the boundary points
    """

    metrics = {
        ("x",): ["Δx_caa", "Δx_faa"], # X distances
        ("y",): ["Δy_aca", "Δy_afa"], # Y distances
        ("z",): ["Δz_aac", "Δz_aaf"], # Z distances
    }

    return metrics


def get_grid(ds, coords=None, metrics=None, topology="PPN", **kwargs):
    """ Gets xgcm grid for ds """
    import xgcm as xg

    if coords is None:
        coords = get_coords(topology)
    if metrics is None:
        metrics = get_metrics(ds, topology=topology)

    periodic = [ dim for (dim, top) in zip("xyz", topology) if top in "PF" ]
    return xg.Grid(ds, coords=coords, metrics=metrics, 
                   periodic=periodic, **kwargs)


