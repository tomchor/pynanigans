
def get_coords(ds, topology="PPN",):
    """ 
    Constructs the coords dict for ds to be passed to xgcm.Grid
    Flat dimensions (F) are treated the same as Periodic ones (P)
    """
    per = dict(left='xF', center='xC')
    nper = dict(outer='xF', center='xC')
    per = { dim : dict(left=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    nper = { dim : dict(outer=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    coords = { dim : per[dim] if top in "FP" else nper[dim] for dim, top in zip("xyz", topology) }
    
    return coords

def get_distances(ds, dim="x", topology="P"):
    """
    Get distance metrics for Center and Face points of one specific dimension ξ.
    If the topology of this dimension is periodic, len(ξC)==len(ξF), but if it
    is nonperiodic, then len(ξC)+1==len(ξF).

    Currently deals with stretched domains (where ΔξC!=ΔξF) in an approximated fashion.
    """
    import numpy as np
    import xarray as xr

    #++++ Useful names
    ξF_name = dim+"F"
    ξC_name = dim+"C"
    #----

    #++++ For distances around cell centers things are (I think always) easy
    ΔξC_left = ds[ξF_name].diff(ξF_name).to_numpy()
    ΔξC = xr.DataArray(ΔξC_left, dims = [ξC_name], 
                         coords = {ξC_name : ds.coords[ξC_name].to_numpy()})
    #----

    #++++ Distances around cell faces are a bit more complicated
    ΔξF_interior = ds[ξC_name].diff(ξC_name).to_numpy()
    ΔξF_0 = ds[ξC_name][0] - ds[ξF_name][0]
    ΔξF_left = xr.DataArray(np.insert(ΔξF_interior, 0, ΔξF_0))

    if topology=="P" or topology=="F":
        ΔξF = xr.DataArray(ΔξF_left, dims = [ξF_name], 
                           coords = {ξF_name : ds.coords[ξF_name].to_numpy()})
    elif topology=="N":
        ΔξF_right = ds[ξF_name][-1] - ds[ξC_name][-1]
        ΔξF_all = xr.DataArray(np.append(ΔξF_left, ΔξF_right))
        ΔξF = xr.DataArray(ΔξF_all, dims = [ξF_name], 
                           coords = {ξF_name : ds.coords[ξF_name].to_numpy()})

    #----

    return xr.Dataset({f"Δ{dim}C" : ΔξC, f"Δ{dim}F" : ΔξF})



def get_metrics(ds, topology="PPN"):
    """ 
    Constructs the metric dict for ds.
    (Not sure if the metrics are correct at the boundary points
    """

    for ξ, top in zip('xyz', topology):
        ξdist = get_distances(ds, dim=ξ, topology=top)
        ds.coords[f"Δ{ξ}C"] = ξdist[f"Δ{ξ}C"]
        ds.coords[f"Δ{ξ}F"] = ξdist[f"Δ{ξ}F"]

    metrics = {
        ('x',): ['ΔxC', 'ΔxF'], # X distances
        ('y',): ['ΔyC', 'ΔyF'], # Y distances
        ('z',): ['ΔzC', 'ΔzF'], # Z distances
    }

    return metrics


def get_grid(ds, coords=None, metrics=None, topology="PPN", **kwargs):
    """ Gets xgcm grid for ds """
    import xgcm as xg

    if coords is None:
        coords = get_coords(ds, topology=topology)
    if metrics is None:
        metrics = get_metrics(ds, topology=topology)

    periodic = [ dim for (dim, top) in zip("xyz", topology) if top in "PF" ]
    return xg.Grid(ds, coords=coords, metrics=metrics, 
                   periodic=periodic, **kwargs)


