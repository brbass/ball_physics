import numpy as np

class Plane:
    """Represents a plane in 2D"""
    
    def __init__(self,
                 origin,
                 normal):
        self.origin = np.array(origin)
        self.normal = np.array(normal)
        return

    def intersection(self, position, direction):
        k0 = self.origin - position
        l0 = np.dot(k0, self.normal)
        l1 = np.dot(direction, self.normal)
        
        if l1 < 1.0e-20:
            # Ball is parallel to plane
            return False, np.inf, self.origin
        
        # Get the distance to intersection
        s = l0 / l1

        if s < 0:
            # Ball would only hit plane if it went backwards
            return False, s, self.origin

        # Get position of intersection
        x = position + direction * s
        
        return True, s, x
    
    def reflected_direction(self, position, direction):
        return direction - 2 * np.dot(direction, self.normal) * self.normal

class Box:
    """A box with four reflecting boundaries"""

    def __init__(self, left, right, bottom, top, reflect=True):
        self.lower = [Plane(origin = [left, 0.0],
                            normal = [-1.0, 0.0]),
                      Plane(origin = [0.0, bottom],
                            normal = [0.0, -1.0])]
        self.upper = [Plane(origin = [right, 0.0],
                            normal = [1.0, 0.0]),
                      Plane(origin = [0.0, top],
                            normal = [0.0, 1.0])]
        self.boundaries = self.lower + self.upper
        self.reflect = reflect
        self.offsets = np.zeros((4, 2))
        for d in range(2):
            self.offsets[d][d] = self.upper[d].origin[d] - self.lower[d].origin[d]
            self.offsets[d+2][d] = -self.offsets[d][d]
        return

    def limits(self, d):
        return [self.lower[d].origin[d], self.upper[d].origin[d]]
    
    def check_inside(self, balls):
        """Make sure all the balls start inside the box"""
        for b in balls:
            for d in range(2):
                if b.position[d] - b.radius < self.lower[d].origin[d] or b.position[d] + b.radius > self.upper[d].origin[d]:
                    raise ValueError("Ball is outside of the box!")
        return
    
    def partial_update(self, position, direction, distance, radius):
        """Update through a single intersection"""
        # Get all the possible intersection events
        events = [b.intersection(position, direction) for b in self.boundaries]
        
        # Find which event happens first
        min_event = -1
        min_dist = np.inf
        for i, e in enumerate(events):
            if e[0]:
                # We have an intersection in the future
                if self.reflect:
                    actual_dist = e[1] - radius / np.abs(np.dot(self.boundaries[i].normal, direction))
                else:
                    actual_dist = e[1]
                if actual_dist < min_dist:
                    min_event = i
                    min_dist = actual_dist

        # We don't intersect, which should never happen!
        if min_event < 0:
            raise ValueError("No intersection found: is a ball outside the box?")

        # Intersection happens after the prescribed distance
        if distance < min_dist:
            position += distance * direction
            distance = 0.0
            return position, direction, distance
        
        # We intersect and want to apply a reflection
        event = events[min_event]
        boundary = self.boundaries[min_event]
        if min_dist < -0.25 * radius:
            raise ValueError("Collision distance negative: is a ball inside the wall?")

        # We have a real collision!
        position += min_dist * direction
        distance -= min_dist
        if self.reflect:
            # Reflecting boundary condition
            direction = boundary.reflected_direction(position, direction)
        else:
            # Periodic boundary condition
            position += self.offsets[min_event]
            
        return position, direction, distance
        
    def update_position(self, x, dx, radius):
        """Update to new position, including possibly multiple boundary collisions"""
        distance = np.linalg.norm(dx)
        direction = dx / distance
        checksum = 0
        while distance > 0.0:
            x, direction, distance = self.partial_update(x, direction, distance, radius)
            checksum += 1
            if checksum > 1000:
                raise ValueError("Too many boundary iterations! Your balls are moving too quickly.")
        return x, direction
