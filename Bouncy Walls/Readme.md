# Bouncy Walls

Consider a rectangular room of integer dimensions. Furthermore, let us be located at (a,b) and an enemy at (x,y) (again, all integers). We possess a lazer, which fires a ray of max
distance before becoming harmless. Furthermore, the walls of this room bounce our rays (mirrors). We wish to find all the possible ways of shooting the enemy located at (x,y) without
shooting ourselves. That is, our algorithm receives as input the dimensions (h,w) of the room and the two coordinates (a,b) and (x,y) and we return the number of possible shooting angles
which result in a enemy hit. We are always located on the integer grid-lattice formed within the room.

## Example
dimensions = [3,2]
yourLoc = [1,1]
enemyLoc = [2,1]
distance = 4 

Result = 7.

Albeit harder to visualize, our hits are:
* 1 hit for shooting directly at him (1,0)
* 2 hits by shooting 45 degrees to the right [(1,2) and (1,-2)]
* 2 hits shooting at a different angle to the right [(3,2) and (3,-2)]
* 2 hits shooting doing the same, to the left this time [(-3,2) and (-3,-2)]

## Solution

It can be quite difficult to figure out the geometry in this problem, with rays bouncing left and right, constantly changing angles. However, rather than focusing exclusively on our single room,
we can instead expand it by considering its 'mirrored' rooms and copy pasting them side by side. This simplifies the problem, as we then simply search for straight lines within this 'expanded' space.
We then loop through those mirrored rooms, checking if we hit the enemy (before ourselves) while also inspecting the ray's length (and comparing them with the max distance). 
