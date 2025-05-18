using Oceananigans
grid = RectilinearGrid(size=(4, 4, 4), extent=(1, 1, 1));
model = NonhydrostaticModel(; grid)
simulation = Simulation(model; Δt = 1, stop_time=10)
simulation.output_writers[:nc] = NetCDFWriter(model, model.velocities, schedule=IterationInterval(1), filename="uvw.nc", overwrite_existing=true)
run!(simulation)
