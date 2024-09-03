from Ball import Ball
from Physics import Gravity
from Simulation import Simulation

import numpy as np

# Input data
include_moon = False
normalize_radii = True

# Convenience function
def find_index(search, descriptions):
    for i, d in enumerate(descriptions):
        if search.lower() in d.lower():
            return i
    raise ValueError("no index found for {}".format(search))
    return -1

# Create our balls
radius_multiplier = 3.0e3
balls = []
with open("SolarSystemData.txt") as f:
    # Find the indices of various data points
    descriptions = f.readline().split('\t')
    fields = {v:find_index(v, descriptions) for v in ["body", "distance", "mass", "diameter", "orbitalvelocity", "color"]}

    # Parse the file
    for l in f:
        data = l.strip().split('\t')
        name = data[fields["body"]].lower()
        if not include_moon and name == "moon":
            continue
        balls.append(Ball(position = [float(data[fields["distance"]]), 0.0],
                          velocity = [0.0, float(data[fields["orbitalvelocity"]])],
                          mass = float(data[fields["mass"]]),
                          radius = 0.5 * float(data[fields["diameter"]]),
                          color = "#{}".format(data[fields["color"]]),
                          name = name))
mean_radius = np.mean([b.radius for b in balls if b.name != "sun"])
for b in balls:
    b.radius *= radius_multiplier
    if normalize_radii and b.name != "sun":
        b.radius = (b.radius + 2 * mean_radius) / 3
        
# Create the physics
physics = [Gravity()]

# Set the limits of the plot to be just outside the chosen planet
outer_lims = "pluto"
outer_index = -1
for i, b in enumerate(balls):
    if b.name == outer_lims:
        outer_index = i
        break
if outer_index == -1:
    raise ValueError("Planet not found")
lim = 1.1 * (balls[outer_index].position[0] + balls[outer_index].radius)
limits = [[i * lim for i in [-1, 1]] for j in range(2)]

# Create the simulation
simulation = Simulation(balls, physics, limits=limits)

# Set time step to a quarter of a day if moon is included or 10 days if not
one_day = 24.0 * 3600.0
simulation.time_step = one_day if include_moon else 10.0 * one_day

# Set number of time steps such that end time is equal to four earth years or one Pluto year
num_years = 4 if include_moon else 248
simulation.num_time_steps = int(num_years * 365.0 * one_day / simulation.time_step)

# Visualize less often to speed things up: try setting to 100 to get through the whole simulation quickly
simulation.visualization_step = 2 if include_moon else 10

# Run the simulation!
simulation.run()
    
