Introduction
============

This is a simple set of physics packages that work on balls, written for beginning programmers to get some experience with physics simulations. Performance isn't stressed; the algorithms for gravity, collision, and electric charge are all N^2 for the number of balls N.

To run the code, create a list of balls, a list of physics packages, optionally a bounding box, and then a simulation. By default, all the units are SI. 

Examples
========

The first example is the solar system, in ``SolarSystem.py``. The radii for that problem are significantly normalized so that we can actually see all the planets.

``python3 SolarSystem.py``

The second example is a set of bouncy balls. It includes gravity pulling the balls straight down and collision between the balls. Note that no energy is lost in collisions, so eventually the added energy from gravity will make the balls go very fast!

``python3 BouncyBalls.py``

The third example is a few electrons and ions floating around in a constant magnetic field.

``python3 MagneticRotation.py``

Exercises
=========

For the following exercises, create a new file for each, import the needed classes, and follow the instructions. 

Exercise 1: A single bouncy ball!
---------------------------------

This exercise creates a ball bouncing about a box. 

1. Create a ball at position x = 0.5, y = 0.9 with velocity vx = 0.7, vy = 0.0.
2. Make a list with only one thing in it: the ball!
3. Create a list with gravity in it using the ConstantAcceleration class.
4. Create a bounding box with 0 <= x,y <= 1 that reflects the ball.
5. Create a simulation and set the time step to 0.02.
6. Run the simulation.

If you need help, look at the example in BouncyBalls.py. Some extensions for this exercise:
- Add additional balls.
- Add collision physics.

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

1. Create balls representing the three bodies. Put them in a line, meaning that the y component should be zero (e.g. position = [-1.62e9, 0.0]). The velocities should be in the y direction (e.g. velocity = [0.0, 9.68e4]). Make sure one of the suns has a negative y velocity so they are spinning around each other. The radii don't matter to the gravity calculation, so make them relatively big so you can see them (maybe three times larger than listed!).
2. Create gravity physics.
3. Create a simulation. Set the limits for plotting to be just larger than the position of tatooine [[-position, position], [-position, position]]. Set the time step to 2 hours (in seconds!).
4. Run the simulation.

Extensions:
- Make the suns spin in the opposite direction by making the starting velocities negative. 
- Make the system stand still in our coordinate system. The system is moving upward with a velocity of (9.68e4 * 3.07e30 - 9.68e4 * 9.09e29 + 4.11e4 * 2.93e24) / (3.07e30 + 9.09e29 + 2.93e24) = 5.26e4 m /s. Subtract that amount from each of the y components of the initial velocities. 
