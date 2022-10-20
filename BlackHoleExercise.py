from Ball import Ball
from Boundary import Box
from Physics import Physics, Gravity
from Simulation import Simulation

import numpy as np

class BlackHoleGravity(Gravity):
    def __init__(self, ball):
        super().__init__()
        self.black_hole = ball
        return

    def set_simulation(self, simulation):
        self.simulation = simulation
        return
    
    def pre_step_update(self, balls, time_step):
        deleteme = list()
        for i, b in enumerate(balls):
            if b is self.black_hole:
                continue
            dist = self.black_hole.distance(b)
            escape_velocity = np.sqrt(2 * self.G * self.black_hole.mass / dist)
            if dist < self.black_hole.radius:
                self.black_hole.velocity = (self.black_hole.mass * self.black_hole.velocity + b.mass * b.velocity) / (self.black_hole.mass + b.mass)
                self.black_hole.mass += b.mass
                self.black_hole.radius = np.power(b.radius ** 3 + self.black_hole.radius ** 3, 1.0/3.0)
                print("---eating ball ", i, "---")
                deleteme.append(i)
            elif np.linalg.norm(b.velocity) > escape_velocity and dist > 50 * self.black_hole.radius:
                print("---ball ", i, " has escaped---")
                deleteme.append(i)
        for i in sorted(deleteme, reverse = True):
            del balls[i]
        simulation.initialize_visualization(True)
        return

# Input data
num_balls = 50
xlim = 1.0e12
xboxlim = 1.5 * xlim
max_mass = 1.0e33
max_radius = 2 * xlim / 40

# Get gravitational constant
G = Gravity().G

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
    b.velocity *= np.sqrt(G * balls[0].mass / dist_from_center)

    # Perturb the velocity a bit to make the orbits elliptical
    b.velocity *= np.random.uniform(0.8, 1.2)

black_hole = BlackHoleGravity(balls[0])
physics = [black_hole]

# Limits for visualization
limits = [[-xboxlim, xboxlim], [-xboxlim, xboxlim]]

# Simulation
simulation = Simulation(balls, physics, limits=limits)
simulation.time_step = 20 * 60.0
simulation.num_time_steps = 1000
simulation.visualization_step = 2
black_hole.set_simulation(simulation)

# Run simulation
simulation.run()

