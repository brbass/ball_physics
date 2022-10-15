from Ball import Ball
from Physics import Charge, Gravity
from Simulation import Simulation

import numpy as np

num_balls = 200
balls = [Ball() for i in range(num_balls)]
for b in balls:
    b.randomize()

star_mult = 1.0e1
balls[0].mass *= star_mult
balls[0].size *= np.power(star_mult, 1./3.)
    
physics = [Gravity()]

simulation = Simulation(balls, physics)
simulation.time_step = 10.0
simulation.num_time_steps = 100

simulation.run()

