------------
Introduction
------------

This is a simple set of physics packages that work on balls, written for beginning programmers to get some experience with physics simulations. Performance isn't stressed; the algorithms for gravity, collision, and electric charge are all N^2 for the number of balls N.

To run the code, create a list of balls, a list of physics packages, optionally a bounding box, and then a simulation. By default, all the units are SI. 

--------
Examples
--------

The first example is the solar system, in ``SolarSystem.py``. The radii for that problem are significantly normalized so that we can actually see all the planets.

``python3 SolarSystem.py``

The second example is a set of bouncy balls. It includes gravity pulling the balls straight down and collision between the balls. Note that no energy is lost in collisions, so eventually the added energy from gravity will make the balls go very fast!

``python3 BouncyBalls.py``

The third example is a few electrons and ions floating around in a constant magnetic field.

``python3 MagneticRotation.py``
