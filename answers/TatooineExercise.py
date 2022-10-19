from Ball import Ball
from Physics import Gravity
from Simulation import Simulation

balls = [Ball(position = [-1.62e9, 0.0],
              velocity = [0.0, 4.42e4],
              mass = 3.07e30,
              radius = 1.07e9*3,
              color = "#de2d26",
              name = "Tatoo I"),
         Ball(position = [5.48e9, 0.0],
              velocity = [0.0, -9.68e4],
              mass = 9.09e29,
              radius = 7.10e8 * 3,
              color = "#9ecae1",
              name = "Tatoo I"),
         Ball(position = [1.65e11, 0.0],
              velocity = [0.0, 4.11e4],
              mass = 2.93e24,
              radius = 5.00e6 * 5.0e1,
              color = "#fed9a6",
              name = "Tatooine")]

physics = [Gravity()]

lim = 1.1 * balls[-1].position[0]
limits = [[-lim, lim], [-lim, lim]]
simulation = Simulation(balls, physics, limits=limits)
simulation.time_step = 2.0 * 3600.0

simulation.run()
