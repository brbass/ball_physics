from Ball import Ball
from Physics import ConstantElectromagneticField, Charge, Drag
from Simulation import Simulation

num_balls = 10
balls = [Ball() for i in range(num_balls)]
for i, b in enumerate(balls):
    b.charge = -1.0e-5
    b.velocity[0] = 1.0
    b.position[1] = i * 2.0
    b.radius = 0.5

physics = [ConstantElectromagneticField(B=1.0e5),
           Drag(quadratic=0.01),
           Charge()]

lim = num_balls * 2.0 + 1.0
simulation = Simulation(balls, physics,
                        limits=[[-lim, lim],
                                [-0.5 * lim, 1.5 * lim]])
simulation.time_step = 0.2
simulation.num_time_steps = 1001
simulation.max_dv = 1.0e10
simulation.visualization_step = 5

simulation.run()
