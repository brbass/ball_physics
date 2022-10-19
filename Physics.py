import numpy as np

class Physics:
    """Base class for all physics"""

    def pre_step_update(self, balls):
        """This runs before the forces are calculated; defaults to doing nothing"""
        return

class BallEnvironmentPhysics(Physics):
    """Base class for physics involving the interaction of a ball with its environment"""
    
    def add_force(self,
                  balls,
                  forces):
        """Add a force between the ball and its environment"""
        num_balls = len(balls)
        for i in range(num_balls):
            forces[i][:] += self.force_be(balls[i])
        return
    
class ConstantAcceleration(BallEnvironmentPhysics):
    """Adds a constant acceleration like gravity"""
    def __init__(self, acceleration = [0.0, -9.81]):
        # Set by default to gravitational constant, https://en.wikipedia.org/wiki/Gravity_of_Earth
        self.acceleration = np.array(acceleration) # m / s^2 
        return

    def force_be(self, balli):
        return self.acceleration * balli.mass

class ConstantElectromagneticField(BallEnvironmentPhysics):
    """Adds a background electromagnetic field"""
    def __init__(self,
                 E = [0.0, 0.0],
                 B = 1.0): 
        self.E = E # m kg / (s^3 A)
        self.B = B # kg / (s^2 A)
        return

    def force_be(self, balli):
        v_cross_B = self.B * np.array([balli.velocity[1], -balli.velocity[0]])
        return balli.charge * (self.E + v_cross_B)

class Drag(BallEnvironmentPhysics):
    """Adds drag for problems where velocities would otherwise increase forever"""
    def __init__(self,
                 linear = 0.0,
                 quadratic = 0.0001):
        self.linear = linear
        self.quadratic = quadratic
        return

    def force_be(self, balli):
        velocity_mag = np.linalg.norm(balli.velocity)
        if velocity_mag < 1.0e-20:
            return np.zeros_like(balli.velocity)
        direction = -balli.velocity / velocity_mag
        return direction * velocity_mag * (self.linear + velocity_mag * self.quadratic)
    
class BallBallPhysics(Physics):
    """Base class for physics involving the interactions of two balls"""
    
    def add_force(self,
                  balls,
                  forces):
        """Add a force between the ball and another ball"""
        num_balls = len(balls)
        for i in range(num_balls):
            for j in range(i+1, num_balls):
                # Get the force on ball i from ball j
                forceij = self.force_bb(balls[i], balls[j])

                # Equal and opposite forces
                forces[i][:] += forceij
                forces[j][:] -= forceij
        return
    
class R2Physics(BallBallPhysics):
    """Base class for charge and gravity physics"""

    def force_bb(self, balli, ballj):
        # Get the direction of the force
        r = balli.position - ballj.position
        
        # r^2 = (x1-x2)^2 + (y1-y2)^2
        r2 = np.dot(r, r)
        
        # rhat = r / r^2
        rhat = r / np.sqrt(r2)
        
        # Force (from descendant classes)
        return self.force_r2_coeff(balli, ballj) * rhat / r2

class Charge(R2Physics):
    """Calculates the electrostatic force between two charged particles"""
    
    def __init__(self):
        # Coulomb constant
        # https://en.wikipedia.org/wiki/Coulomb_constant
        self.k = 8.9875517921e9 # kg m^3 s^-4 A^-2
        return
    
    def force_r2_coeff(self, balli, ballj):
        # F = q1 * q2 / (4 * pi * e0) * rhat / r^2
        # https://en.wikipedia.org/wiki/Coulomb%27s_law#Vector_form_of_the_law
        return self.k * balli.charge * ballj.charge
    
class Gravity(R2Physics):
    """Calculates the gravitational force between two objects"""
    def __init__(self):
        # Gravitational constant
        # https://en.wikipedia.org/wiki/Gravitational_constant
        self.G = 6.67430e-11 # N m^2 kg^-2
        return

    def force_r2_coeff(self, balli, ballj):
        # F = -G * m1 * m2 * rhat / r^2
        # https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Vector_form
        return -self.G * balli.mass * ballj.mass

class Collision(BallBallPhysics):
    """Calculates collision between balls"""

    def __init__(self,
                 evolve_spring_constant = False,
                 spring_constant = 1.e5):
        self.evolve_spring_constant = evolve_spring_constant
        self.spring_constant = spring_constant # kg / s^2
        return

    def pre_step_update(self, balls):
        if self.evolve_spring_constant:
            average_mass = np.mean([b.mass for b in balls])
            max_velocity = np.amax([np.linalg.norm(b.velocity) for b in balls])
            min_radius = np.amin([b.radius for b in balls])

            self.spring_constant = average_mass * (max_velocity / min_radius) ** 2
        return
        
    def force_bb(self, balli, ballj):
        # Vector from center of one ball to center of the other
        r = balli.position - ballj.position

        # Distance between balls
        dist = np.sqrt(np.dot(r, r))

        # Check whether balls overlap
        overlap = balli.radius + ballj.radius - dist
        if (overlap < 0):
            # Distance between balls is greater than their combined radii, so no overlap!
            return 0.0
        
        # Normalize the vector
        rhat = r / dist
        
        # Hooke's law!
        return self.spring_constant * overlap * rhat
    
