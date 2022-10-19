from Ball import Ball
from Boundary import Box
from Physics import ConstantAcceleration, Drag
from Simulation import Simulation

include_drag = False

ball = Ball(position = [0.5, 0.9],
            velocity = [0.7, 0.0])
balls = [ball]

physics = [ConstantAcceleration()]
if include_drag:
    physics.append(Drag(linear=0.5, quadratic=0.0))

box = Box(0,1,0,1, reflect=True)

simulation = Simulation(balls, physics, box)
simulation.time_step = 0.02
simulation.visualization_step = 2

simulation.run()
