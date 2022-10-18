from Ball import Ball
from Physics import Gravity
from Simulation import Simulation

import numpy as np

# Create balls representing the planets with their appropriate masses
def getSolarSystem(randomize_position = False,
                   normalize_radii = True,
                   radius_multiplier = 5.0e2,
                   include_moon = False):
    # From https://nssdc.gsfc.nasa.gov/planetary/factsheet/ and https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
    names = ["sun", "venus", "mercury", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "moon"]
    positions = 1.0e9 * np.array([0.0, 5.79E+01,1.08E+02,1.50E+02,2.28E+02,7.79E+02,1.43E+03,2.87E+03,4.52E+03,5.91E+03,0.384])
    masses = 1.0e24 * np.array([1.9885e6, 3.30E-01,4.87E+00,5.97E+00,6.42E-01,1.90E+03,5.68E+02,8.68E+01,1.02E+02,1.30E-02,7.30E-02])
    radii = radius_multiplier * 1.0e3 * np.array([6.957e5, 4.88E+03,1.21E+04,1.28E+04,6.79E+03,1.43E+05,1.21E+05,5.11E+04,4.95E+04,2.38E+03,3.48E+03])
    velocities = 1.0e3 * np.array([0.0, 4.74E+01,3.50E+01,2.98E+01,2.41E+01,1.31E+01,9.70E+00,6.80E+00,5.40E+00,4.70E+00,1.0])
    colors = ["#ffffff","#bdbdbd","#feb24c","#31a354","#ff9d6f","#8c2d04","#fee391","#ace5ee","#2171b5","#f6e8c3","#636363"]
    num_bodies = len(positions) if include_moon else len(positions) - 1
    
    if normalize_radii:
        norm_factor = 3
        radii = np.divide(radii + norm_factor * np.mean(radii) / 2, norm_factor + 1)
        
    # Add the bodies
    bodies = []
    for i in range(num_bodies):
        position = [positions[i], 0.0]
        velocity = [0.0, velocities[i]]
        bodies.append(Ball(position = position,
                           velocity = velocity,
                           mass = masses[i],
                           radius = radii[i],
                           color = colors[i],
                           name = names[i]))
        
    if include_moon:
        # Put the moon around the earth
        bodies[-1].position += bodies[3].position
        bodies[-1].velocity += bodies[3].velocity
    
    return bodies


# Create the balls and include gravity
balls = getSolarSystem()
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

# Set time step to 10 days
simulation.time_step = 10.0 * 24.0 * 3600.0

# Set number of time steps equal to the orbital period of Pluto
simulation.num_time_steps = int(248.0 * 365.0 * 24.0 * 3600.0 / simulation.time_step)

# Run the simulation!
simulation.run()
    
