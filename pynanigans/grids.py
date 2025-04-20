
def get_coords(ds, topology="PPN",):
    """ 
    Constructs the coords dict for ds to be passed to xgcm.Grid
    Flat dimensions (F) are treated the same as Periodic ones (P)
    """
    per = dict(left='x_faa', center='x_caa')
    nper = dict(outer='x_faa', center='x_caa')
    per = { dim : dict(left=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    nper = { dim : dict(outer=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    coords = { dim : per[dim] if top in "FP" else nper[dim] for dim, top in zip("xyz", topology) }
    
    return coords


def get_distances(ds, dim="x", topology="P"):
    """
    Get distance metrics for Center and Face points of one specific dimension ξ.
    If the topology of this dimension is periodic, len(ξC)==len(ξF), but if it
    is nonperiodic, then len(ξC)+1==len(ξF).

    Currently does not deal with stretched domains where ΔξC!=ΔξF in the interior.
    """
    import numpy as np
    import xarray as xr

    Δξ_mean = ds[dim+"C"].diff(dim+"C").mean().item()
    ΔξC = xr.DataArray(np.ones(len(ds[dim+"C"])), dims=[dim+'C'])
    if topology=="P" or topology=="F":
        ΔξF = xr.DataArray(np.ones(len(ds[dim+"F"])), dims=[dim+'F'])
    elif topology=="N":
        if len(ds[dim+"F"]) != 1:
            interior = np.ones(len(ds[dim+"F"])-2)
            ΔξF = xr.DataArray(np.hstack([0.5, interior, 0.5]), dims=[dim+'F'])
        else: # Especial case of a slice in a non-periodic dimension
            ΔξF = xr.DataArray([1], dims=[dim+'F'])
    return Δξ_mean * xr.Dataset({f"Δ{dim}C" : ΔξC, f"Δ{dim}F" : ΔξF})


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


