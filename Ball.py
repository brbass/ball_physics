import numpy as np

class Ball:
    def __init__(self,
                 position = [0.0, 0.0],
                 velocity = [0.0, 0.0],
                 mass = 1.0,
                 radius = 0.05,
                 charge = 0.0,
                 color = "#2b8cbe",
                 name = "none"):
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

        # Color of ball for plotting
        self.color = color

        # Name of ball, if desired
        self.name = name
        
        return

    def distance(self, other_ball):
        return np.linalg.norm(self.position - other_ball.position)
    
    def randomize(self,
                  position_range = [0.1, 0.9],
                  velocity_range = [-1.0, 1.0],
                  max_mass = 1.0,
                  max_radius = 0.05,
                  radius_range = 10.0,
                  other_balls = None, # [my_index, ball_list]
                  exclusion_distance = None,
                  recursion = 0):
        if recursion > 100:
            raise ValueError("too much recursion in randomize: are there too many balls for this space?")
        self.position = np.random.uniform(position_range[0], position_range[1], 2)
        velocity_mag = np.random.uniform(velocity_range[0], velocity_range[1])
        heading = np.random.uniform(-1,1,2)
        heading = heading / np.linalg.norm(heading)
        self.velocity = heading * velocity_mag
        radius_mult = np.random.uniform(1.0 / radius_range, 1.0)
        self.mass = max_mass * radius_mult ** 3
        self.radius = max_radius * radius_mult
        self.charge = -1.0e-5 if np.random.randint(0, 2) == 0 else 1.0e-5
        self.color = np.random.rand(3)

        if other_balls is not None:
            for i, b in enumerate(other_balls[1]):
                if i == other_balls[0]:
                    continue
                dist = exclusion_distance if exclusion_distance is not None else self.radius + b.radius
                if self.distance(b) < dist:
                    self.randomize(position_range,
                                   velocity_range,
                                   max_mass,
                                   max_radius,
                                   radius_range,
                                   other_balls,
                                   exclusion_distance,
                                   recursion = recursion + 1)
                    return
        return

        
