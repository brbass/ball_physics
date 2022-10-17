import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections as mc

class Simulation:
    def __init__(self,
                 balls,
                 physics,
                 box = None):
        self.balls = balls
        self.physics = physics
        self.box = box
        
        self.time = 0.0
        self.time_step = 1.0
        self.num_time_steps = 1000

        self.initialize_visualization()
        
        return

    def run(self):
        num_balls = len(self.balls)
        dimension = 2
        for s in range(self.num_time_steps):
            print("step: {}, time: {}, time step: {}".format(s, self.time, self.time_step))

            # Prepare things before calculating the forces
            for p in self.physics:
                p.pre_step_update(self.balls)
            
            # Get the forces on each ball
            forces = np.zeros((num_balls, dimension))
            for p in self.physics:
                p.add_force(self.balls, forces)
            for i, b in enumerate(self.balls):
                # Calculate the acceleration from the force
                # F = m * a, so a = F / m
                acceleration = forces[i][:] / b.mass
                # print(i, b.position, acceleration)
                
                # Increase the velocity
                # v = v0 + dt * a
                b.velocity += self.time_step * acceleration

                # Increase the position
                # x = x0 + dt * v
                self.update_position(b)
                # b.position += self.time_step * b.velocity
                
            # Plot the new state
            self.update_visualization()
            
            # Increment the time
            self.time += self.time_step
        plt.show(block=True)
        return

    def update_position(self, ball):
        dx = ball.velocity * self.time_step

        if self.box is not None:
            # Make sure to take box collisions into account!
            ball.position, direction = self.box.update_position(ball.position, dx, ball.radius)
            ball.velocity = direction * np.linalg.norm(ball.velocity)
            return
        
        # No box: do the usual thing
        ball.position += dx
        return
    
    def get_lim(self, d):
        pos = [b.position[d] for b in self.balls]
        radius = np.amax([b.radius for b in self.balls])
        return [np.amin(pos)- radius, np.amax(pos)+ radius]
    
    def initialize_visualization(self):
        self.fig, self.ax = plt.subplots()
        self.update_visualization()
        plt.show(block=False)
        return
    
    def update_visualization(self):
        self.ax.clear()
        self.patches = [plt.Circle(b.position, b.radius) for b in self.balls]
        self.collection = mc.PatchCollection(self.patches)
        self.ax.add_collection(self.collection)

        if self.box is not None:
            self.ax.set_xlim(self.box.limits(0))
            self.ax.set_ylim(self.box.limits(1))
        else:
            self.ax.set_xlim(self.get_lim(0))
            self.ax.set_ylim(self.get_lim(1))
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlabel("x position (meters)")
        self.ax.set_ylabel("y position (meters)")
        
        plt.draw()
        plt.pause(1.0e-12)

        return
