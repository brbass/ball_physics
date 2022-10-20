import numpy as np
from matplotlib import pyplot as plt
from matplotlib import collections as mc
import time

class Simulation:
    def __init__(self,
                 balls,
                 physics,
                 box = None,
                 limits = None):
        # Input data
        self.balls = balls
        self.physics = physics
        self.box = box
        self.limits = limits

        # Time stepping options
        self.time = 0.0
        self.time_step = 1.0
        self.num_time_steps = 1000

        # Minimum and maximum delta velocity for the time step
        self.min_dv = 0.0
        self.max_dv = np.inf

        # How often we update the visualization and print info
        self.visualization_step = 1
        self.print_step = 20

        # Initialize the kinetic energy
        self.update_kinetic_energy()

        # Track the time to do visualizations
        self.physics_time = 0.0
        self.visualization_time = 0.0
        self.boundary_time = 0.0
        
        # Start up the visualization
        self.initialize_visualization()

        # Print starting message
        self.print_welcome()

        
        return

    def run(self):
        num_balls = len(self.balls)
        dimension = 2
        min_dv = np.inf
        max_dv = 0.0
        print("{:>7} {:>11} {:>11} {:>13}".format("step", "time", "time step", "kin energy"))
        for s in range(self.num_time_steps):
            if s % self.print_step == 0:
                print("{:7} {:11.4g} {:11.4g} {:13.3e}".format(s, self.time, self.time_step, self.kinetic_energy))
            
            # Start our timer
            timer = time.perf_counter()
            
            # Prepare things before calculating the forces
            for p in self.physics:
                physics_timer = time.perf_counter()
                p.pre_step_update(self.balls, self.time_step)
                p.physics_time += time.perf_counter() - physics_timer
            
            # Get the forces on each ball
            forces = np.zeros((num_balls, dimension))
            for p in self.physics:
                physics_timer = time.perf_counter()
                p.add_force(self.balls, forces)
                p.physics_time += time.perf_counter() - physics_timer
            for i, b in enumerate(self.balls):
                # Calculate the acceleration from the force
                # F = m * a, so a = F / m
                acceleration = forces[i][:] / b.mass
                
                # Increase the velocity
                # v = v0 + dt * a
                dv = self.time_step * acceleration
                b.velocity += dv

                # Increase the position
                # x = x0 + dt * v
                self.update_position(b)
                # b.position += self.time_step * b.velocity
                
                # Adjust the time step, if needed
                dvmag = np.linalg.norm(dv)
                min_dv = min(min_dv, dvmag)
                max_dv = max(max_dv, dvmag)
                if (min_dv < self.min_dv):
                    self.time_step *= 2.0
                elif max_dv > self.max_dv:
                    self.time_step *= 0.5
                    
            # Update the kinetic energy
            self.update_kinetic_energy()

            # Add to our time
            self.physics_time += time.perf_counter() - timer
            
            # Plot the new state
            if (s + 1) % self.visualization_step == 0:
                self.update_visualization()
            
            # Increment the time
            self.time += self.time_step
        self.print_timers()
        plt.show(block=True)
        return

    def update_position(self, ball):
        dx = ball.velocity * self.time_step

        if self.box is not None:
            timer = time.perf_counter()
            # Make sure to take box collisions into account!
            ball.position, direction = self.box.update_position(ball.position, dx, ball.radius)
            ball.velocity = direction * np.linalg.norm(ball.velocity)
            self.boundary_time += time.perf_counter() - timer
            return
        
        # No box: do the usual thing
        ball.position += dx
        return

    def update_kinetic_energy(self):
        self.kinetic_energy = 0.0
        for b in self.balls:
            self.kinetic_energy += 0.5 * b.mass * np.dot(b.velocity, b.velocity)
        return

    def get_lim(self, d):
        pos = [b.position[d] for b in self.balls]
        radius = np.amax([b.radius for b in self.balls])
        return [np.amin(pos)- radius, np.amax(pos)+ radius]
    
    def initialize_visualization(self, reinitialize = False):
        timer = time.perf_counter()
        
        if reinitialize:
            self.ax.clear()
        else:
            plt.style.use('dark_background')
            self.fig, self.ax = plt.subplots(dpi=150)
        self.patches = [plt.Circle(b.position, b.radius, color=b.color) for b in self.balls]
        self.collection = mc.PatchCollection(self.patches, match_original=True)
        self.ax.add_collection(self.collection)
        self.set_limits(True)
        plt.show(block=False)
        
        self.visualization_time += time.perf_counter() - timer
        
        return
    
    def update_visualization(self):
        timer = time.perf_counter()

        for b, c in zip(self.balls, self.patches):
            c.center = b.position
        self.collection.set_paths(self.patches)
        self.set_limits()
        self.fig.canvas.flush_events()
        plt.show(block=False)
        # plt.pause(0.1)

        self.visualization_time += time.perf_counter() - timer

        return

    def set_limits(self, first_time = False):
        dynamic_limits = self.limits is None and self.box is None

        # Set limits
        if first_time and not dynamic_limits:
            # These don't change during the simulation
            if self.limits is not None:
                self.ax.set_xlim(self.limits[0])
                self.ax.set_ylim(self.limits[1])
            elif self.box is not None:
                self.ax.set_xlim(self.box.limits(0))
                self.ax.set_ylim(self.box.limits(1))
        elif dynamic_limits:
            # This changes each step
            self.ax.set_xlim(self.get_lim(0))
            self.ax.set_ylim(self.get_lim(1))

        # Set labels
        if first_time:
            self.ax.set_xlabel("x position (meters)")
            self.ax.set_ylabel("y position (meters)")

        # Set aspect ratio equal
        if first_time or dynamic_limits:
            self.ax.set_aspect('equal', adjustable='box')
            
        return
            
    def print_welcome(self):
        print(" oooooooooooooooooooooooooooooo")
        print(" oooooo  Ball Simulator  oooooo")
        print(" oooooooooooooooooooooooooooooo")
        self.print_unicorn()
        return
    
    def print_timers(self):
        print()
        print(" ----------------------------- ")
        print("          Timing info          ")
        print(" ----------------------------- ")
        print("Physics: ", self.physics_time)
        for p in self.physics:
            print("    {}: ".format(p.__class__.__name__), p.physics_time)
        print("    Boundary: ", self.boundary_time)
        print("Visualization: ", self.visualization_time)
        return
    
    def print_unicorn(self):
        # Print glorious art to inspire the user (https://www.asciiart.eu/mythology/unicorns)
        print("""
               |))    |))
 .             |  )) /   ))
 \\   ^ ^      |    /      ))
  \\(((  )))   |   /        ))
   / G    )))  |  /        ))
  |o  _)   ))) | /       )))
   --' |     ))`/      )))
    ___|              )))
   / __\             ))))`()))
  /\@   /             `(())))
  \/   /  /`_______/\   \  ))))
       | |          \ \  |  )))
       | |           | | |   )))
       |_@           |_|_@    ))
       /_/           /_/_/
        """)
        return
