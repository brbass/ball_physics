Introduction
============

This is a simple set of physics packages that work on balls, written for beginning programmers to get some experience with physics simulations. Performance isn't stressed; the algorithms for gravity, collision, and electric charge are all N^2 for the number of balls N. The visualization is usually the bottleneck. 

To run the code, create a list of balls, a list of physics packages, optionally a bounding box, and then a simulation. By default, all the units are SI. 

Examples
========

Example 1: Solar system
-----------------------

The first example is the solar system, in ``SolarSystem.py``. The radii for that problem are significantly normalized so that we can actually see all the planets.

``python3 SolarSystem.py``

Example 2: Bouncy balls
-----------------------

The second example is a set of bouncy balls. It includes gravity pulling the balls straight down and collision between the balls. The kinetic energy will go up and down, but the total energy (gravitational potential plus kinetic) should stay the same.

``python3 BouncyBalls.py``

Example 3: Magnetic rotation
----------------------------

The third example is a few electrons and ions floating around in a constant magnetic field.

``python3 MagneticRotation.py``

Exercises
=========

For the following exercises, create a new file for each, import the needed classes, and follow the instructions. 

Exercise 1: A single bouncy ball
--------------------------------

This exercise creates a ball bouncing about a box. 

1. Create a ball at position x = 0.5, y = 0.9 with velocity vx = 0.7, vy = 0.0. Keep the mass at its default setting.
2. Make a list with only one thing in it: the ball!
3. Create a list with gravity in it using the ConstantAcceleration class.
4. Create a bounding box with 0 <= x,y <= 1 that reflects the ball.
5. Create a simulation and set the time step to 0.02.
6. Run the simulation.

If you need help, look at the example in BouncyBalls.py and try to change it as listed above. If you get really stuck, the solution is in `SingleBallExercise.py`.

Some extensions for this exercise:
- Add additional balls.
- Add collision physics.
- Add drag to simulate the balls running into air (try a linear coefficient of 0.5 and a quadratic coefficient of 0.0). What changes about the simulation?

Exercise 2: Tatooine
--------------------

Tatooine is a planet in star Wars that orbits twin stars, Tatoo I and Tatoo II.

The information on the site https://www.theforce.net/swtc/orbs.html#tatooine indicates the following (rounded for simplicity). You can skip this unless you're interested! 

- The ratio of the diameters of the suns is 15:10.
- The two stars combined have twice the mass of the sun (1.99e30 kg), with ratios 15^3 to 10^3 (or 3.375 to 1) from the diameters above.
- The separation is 10 times the radius of the smaller star and is equal to 7.1e9 m. Let [0.0, 0.0] be the center of mass for the problem to calculate the starting positions in the table below.
- The diameter of Tatooine is around 1.0e7 m, so the mass (scaling off of the earth) is 6e24 * (1.0e7 / 1.27e7)^3 = 2.93e24 kg
- The suns orbit each other in around 64 hours, meaning that the suns are going pi * 7.1e9 m in 64 * 3600 seconds, or 9.68e4 m/s
- Tatooine orbits at 1.1 au = 1.65e11 m every 0.8 earth years, so it goes 2 * pi * 1.65e11 meters in 0.8 * 365 * 24 * 3600 seconds, or 4.11e4 m/s.

Here is the input parameters that we will be using, based off of the above data:

======== ====== ======== ======= ========
Body     Radius Velocity Mass    Position
-------- ------ -------- ------- --------
Tatoo I  1.07e9  9.68e4  3.07e30 -1.62e9
Tatoo II 7.10e8 -9.68e4  9.09e29  5.48e9
Tatooine 5.00e6  4.11e4  2.93e24  1.65e11
======== ====== ======== ======= ========

Do the following to create the input script:

1. Create balls representing the three bodies. Put them in a line, meaning that the y component should be zero (e.g. position = [-1.62e9, 0.0]). The velocities should be in the y direction (e.g. velocity = [0.0, 9.68e4]). Make sure one of the suns has a negative y velocity so they are spinning around each other. The radii don't matter to the gravity calculation, so make them relatively big so you can see them (maybe three times larger than listed for the suns and fifty times larger for Tatooine).
2. Create gravity physics.
3. Create a simulation. Set the limits for plotting to be just larger than the position of tatooine [[-position, position], [-position, position]]. Set the time step to 1 hour (3600 seconds!). If you want to simulate a Tatooine year, set the number of time steps to be 4380. Set simulation.visualization_timestep to something between 1 (slow, lots of frames) and 100 (fast, few frames).
4. Run the simulation.

For help, look at the solar system example. You probably won't need the getSolarSystem function here, as there are only three bodies, but much of the rest should be the same. If you get really stuck, look at `TatooineExercise.py`.

Extensions:
- The orbit of Tatooine is pretty irregular, so Luke is going to be fried before he gets the chance to save the galaxy. That means our initial velocity wasn't high enough and that the website has betrayed us! Try increasing the initial velocity of Tatooine to keep the orbit more regular.
- Subtract around 1.2e4 m/s from all the y components of the velocity to keep the system from moving upward. This happens because the center of mass of the system is moving upwards. 
- Try increasing the time step to 4 hours to see what happens when we try to move the suns too quickly. Turn simulation.visualization_step to 1 to see this, as it happens quickly! 
- Add drag physics to the problem to simulate the suns and planet continually running into death stars (try a quadratic drag coefficient of 1.0e16). Why does the planet essentially stop and the suns keep rotating?
