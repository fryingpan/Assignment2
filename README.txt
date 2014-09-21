Video Game Assignment 2 README
Frying Pan

Katie Chang
Carla Castro
Mary Yen
Josh Holstein

The program accomplishes the requirements for the assignment, in that the
player is controlled by the arrow keys and when the player turns, the ice
cream monsters will turn to face the other way. Otherwise, the monsters
just move randomly.

For the random movement of the enemy, the x and y coordinates are
calculated by multiplying the interval by the speed and
randomly generated angle.

When the player or enemies reach the border of the screen, they can't
advance further since we don't allow them to go beyong the dimensions
of the window. The player also makes a sound each time he bumps into
the window edge as well. This sound is stopped and restarted every time
the player hits the wall.

The game is organized such that it's a class file that's activated by the main,
and then the game updates by the sprite movements by using the sprites' own update
methods.
