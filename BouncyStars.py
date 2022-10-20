from Ball import Ball
from Boundary import Box
from Physics import Collision, Gravity
from Simulation import Simulation

import numpy as np

# Input data
num_balls = 50
xlim = 1.0e12
xboxlim = 1.5 * xlim
max_mass = 1.0e33
max_radius = 2 * xlim / 40

# Get gravity for velocity calculation
gravity = Gravity()
collision = Collision(evolve_spring_constant = True)
physics = [gravity, collision]

# Generate balls
balls = [Ball() for i in range(num_balls)]
balls[0].position[:] = 0.0
balls[0].mass = max_mass * 1.0e2
balls[0].radius = max_radius * 4
for i in range(1, num_balls):
    b = balls[i]
    b.randomize(position_range = [-xlim, xlim],
                max_mass = max_mass,
                max_radius = max_radius,
                radius_range = 4.0,
                other_balls = [i, balls])

    # Calculate stable orbital velocity
    neg_mult = 1.0 #np.random.choice([-1,1])
    b.velocity[0] = -neg_mult * b.position[1]
    b.velocity[1] = neg_mult * b.position[0]
    dist_from_center = np.linalg.norm(b.position)
    b.velocity /= dist_from_center
    b.velocity *= np.sqrt(gravity.G * balls[0].mass / dist_from_center)

    # Perturb the velocity a bit to make the orbits elliptical
    b.velocity *= np.random.uniform(0.8, 1.2)


# Bounding box with periodic boundaries
box = Box(-xboxlim, xboxlim, -xboxlim, xboxlim, reflect=False)

# Simulation
simulation = Simulation(balls, physics, box)
simulation.time_step = 20 * 60.0
simulation.num_time_steps = 1000
simulation.visualization_step = 2

# Run simulation
simulation.run()

