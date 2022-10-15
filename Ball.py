import numpy as np

class Ball:
    def __init__(self,
                 position = [0.0, 0.0],
                 velocity = [0.0, 0.0],
                 mass = 1.0,
                 size = 1.0,
                 charge = 0.0):
        # Where is the ball?
        self.position = np.array(position)
        
        # Where is the ball going?
        self.velocity = np.array(velocity)
        
        # Mass of the ball, which affects gravity and collisions
        self.mass = mass
        
        # Size of the ball, which tells us when two balls collide
        self.size = size
        
        # Charge of the ball, positive or negative, which tells us how particles are attracted
        self.charge = charge

        # Forces on the ball
        self.force = 0.0
        
        return

    def randomize(self):
        dimension = 2
        for d in range(dimension):
            self.position[d] = np.random.uniform(-1.0e9, 1.0e9)
            self.velocity[d] = np.random.uniform(-1.0e6, 1.0e6)
        size_mult = np.random.uniform(0.1, 1.0)
        self.mass = 1.0e28 * size_mult ** 3
        self.size = 1.0e7 * size_mult
        self.charge = -1 if np.random.randint(0, 2) == 0 else 1
        return

        
