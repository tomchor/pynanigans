__version__ = "0.0.0"

def get_grid(ds, topology="PPN", **kwargs):
    import xgcm as xg

    #----
    # Create coord
    per = dict(left='xF', center='xC')
    nper = dict(outer='xF', center='xC')
    per = { dim : dict(left=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    nper = { dim : dict(outer=f"{dim}F", center=f"{dim}C") for dim in "xyz" }
    coords = { dim : per[dim] if top=="P" else nper[dim] for dim, top in zip("xyz", topology) }
    #----

    #----
    grid = xg.Grid(ds, coords=coords,
                   **kwargs)
    #----
    
    return grid

