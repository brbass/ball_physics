from Ball import Ball
from Boundary import Box
from Physics import ConstantAcceleration
from Simulation import Simulation

ball = Ball(position = [0.5, 0.9],
            velocity = [0.7, 0.0])
balls = [ball]

physics = [ConstantAcceleration()]

box = Box(0,1,0,1, reflect=True)

simulation = Simulation(balls, physics, box)
simulation.time_step = 0.02

simulation.run()
