import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections as mc

class Simulation:
    def __init__(self,
                 balls,
                 physics):
        self.balls = balls
        self.physics = physics
        
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
                b.position += self.time_step * b.velocity
                
            # Plot the new state
            self.update_visualization()
            
            # Increment the time
            self.time += self.time_step
        plt.show(block=True)
        return

    def get_lim(self, d):
        pos = [b.position[d] for b in self.balls]
        size = np.amax([b.size for b in self.balls])
        return [np.amin(pos)- size, np.amax(pos)+ size]
    
    def initialize_visualization(self):
        self.fig, self.ax = plt.subplots()
        self.update_visualization()
        plt.show(block=False)
        return
    
    def update_visualization(self):
        self.ax.clear()
        self.patches = [plt.Circle(b.position, b.size) for b in self.balls]
        self.collection = mc.PatchCollection(self.patches)
        self.ax.add_collection(self.collection)
        
        self.ax.set_xlim(self.get_lim(0))
        self.ax.set_ylim(self.get_lim(1))
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlabel("x position (meters)")
        self.ax.set_ylabel("y position (meters)")
        
        plt.draw()
        plt.pause(0.000001)

        return
