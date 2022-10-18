from Ball import Ball
from Boundary import Box
from Physics import Collision, ConstantAcceleration
from Simulation import Simulation

num_balls = 20
balls = [Ball() for i in range(num_balls)]
for b in balls:
    b.randomize(max_radius = 0.05, radius_range = 2.0)

physics = [Collision(), ConstantAcceleration()]

box = Box(0.0, 1.0, 0.0, 1.0, reflect=True)

simulation = Simulation(balls, physics, box)
simulation.time_step = 0.0015
simulation.num_time_steps = 1000

simulation.run()