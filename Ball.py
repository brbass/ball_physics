import numpy as np

class Ball:
    def __init__(self,
                 position = [0.0, 0.0],
                 velocity = [0.0, 0.0],
                 mass = 1.0,
                 radius = 1.0,
                 charge = 0.0):
        # Where is the ball?
        self.position = np.array(position)
        
        # Where is the ball going?
        self.velocity = np.array(velocity)
        
        # Mass of the ball, which affects gravity and collisions
        self.mass = mass
        
        # Radius of the ball, which tells us when two balls collide
        self.radius = radius
        
        # Charge of the ball, positive or negative, which tells us how particles are attracted
        self.charge = charge

        # Forces on the ball
        self.force = 0.0
        
        return

    def randomize(self,
                  position_range = [0.1, 0.9],
                  velocity_range = [-1.0, 1.0],
                  max_mass = 1.0,
                  max_radius = 0.05,
                  radius_range = 10.0):
        for d in range(2):
            self.position[d] = np.random.uniform(position_range[0], position_range[1])
            self.velocity[d] = np.random.uniform(velocity_range[0], velocity_range[1])
        radius_mult = np.random.uniform(1.0 / radius_range, 1.0)
        self.mass = max_mass * radius_mult ** 3
        self.radius = max_radius * radius_mult
        self.charge = -1 if np.random.randint(0, 2) == 0 else 1
        return

        
