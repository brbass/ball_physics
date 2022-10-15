import numpy as np

class Physics:
    """Base class for all physics"""
    
    def __init__(self):
        return

class R2Physics:
    """Base class for charge and gravity physics"""
    
    def __init__(self):
        return

    def add_force(self,
                  balls,
                  forces):
        num_balls = len(balls)
        for i in range(num_balls):
            for j in range(i+1, num_balls):
                # Get the direction of the force
                rij = balls[i].position - balls[j].position
                
                # r^2 = (x1-x2)^2 + (y1-y2)^2
                rij2 = np.dot(rij, rij)

                # rhat = r / r^2
                rhatij = rij / np.sqrt(rij2)

                # Force (from descendant classes)
                forceij = self.forceij(balls[i], balls[j]) * rhatij / rij2
                
                # Equal and opposite forces
                forces[i][:] += forceij
                forces[j][:] -= forceij
        return

class Charge(R2Physics):
    """Calculates the electrostatic force between two charged particles"""
    
    def __init__(self):
        # Coulomb constant
        # https://en.wikipedia.org/wiki/Coulomb_constant
        self.k = 8.9875517921e9 # kg * m^3 * s^-4 * A^-2
        return
    
    def forceij(self, balli, ballj):
        # F = q1 * q2 / (4 * pi * e0) * rhat / r^2
        # https://en.wikipedia.org/wiki/Coulomb%27s_law#Vector_form_of_the_law
        return self.k * balli.charge * ballj.charge
    
class Gravity(R2Physics):
    """Calculates the gravitational force between two objects"""
    def __init__(self):
        # Gravitational constant
        # https://en.wikipedia.org/wiki/Gravitational_constant
        self.G = 6.67430e-11 # N * m^2 * kg^-2
        return

    def forceij(self, balli, ballj):
        # F = -G * m1 * m2 * rhat / r^2
        # https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation#Vector_form
        return -self.G * balli.mass * ballj.mass
        
