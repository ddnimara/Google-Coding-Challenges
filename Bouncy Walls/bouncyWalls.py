def solution(dimensions, your_position, guard_position, distance):
    """ Given dimensions of room, your and the guard's starting position and the laser's
        max harmful distance, returns the number of ways you can shoot and hit the guard
        (considering reflections on walls) without hitting yourself. """
    return len(inspectBlocks(dimensions, your_position, guard_position, distance))

from fractions import Fraction

def positionToVector(your_position, target_position):
    """ Let (x,y) = your position and (a,b) = target location.
        This function returns direction vector (w,v) from (x,y) to (a,b)
        such that (w,v) is 'simplified', that is gcd(w,v) = 1. """

    # compute direction vector [a-x, b-y]
    vector = [0, 0]
    vector[0] = target_position[0] - your_position[0]
    vector[1] = target_position[1] - your_position[1]

    if vector[0] == 0 and vector[1] == 0:  # special case (when shooting yourself at start)
        return vector
    elif vector[0] == 0:  # any (0, b) -> (0,1)
        vector[1] = int(sign(vector[1]))
    elif vector[1] == 0:  # any (a,0) -> (1,0)
        vector[0] = int(sign(vector[0]))
    else:  # use Fraction class to generate (w,v) by considering (b-y)/(a-x) and simplifying it
        simplifiedVector = Fraction(vector[1], vector[0])  # y/x
        vector[0] = int(abs(simplifiedVector.denominator) * sign(vector[0]))
        vector[1] = int(abs(simplifiedVector.numerator) * sign(vector[1]))

    return vector



def inspectBlocks(dimensions, your_position, guard_position, distance):
    """ Main method. Returns a set with all the valid directions that shoot the
        guard but not ourselves."""

    # The gist of the algorithm is that, instead of focusing
    # exclusively on our single room, we can instead expand it
    # by considering its 'mirrored' rooms and copy pasting them
    # side by side. This simplifies the problem, as we then simply
    # search for straight lines within this 'expanded' space.

    # Initialize
    hit_guard = set()
    hit_yourself = set()

    # We loop from the center, outwards. Let (x,y) indicate the (x,y)-th
    # mirrored room. For reference, (0,0) indicates our initial room.
    # We will first loop for x>=0 and then for x<0.
    # For each x, we will loop first y>=0 and then y<0.
    # When we loop this way, we know that if we are inspecting the guard's position
    # in the (x,y) room and find that its vector is (w,v), then if this vector is not located
    # in the hit_guard or hit_yourself set, it is the SHORTEST ray. This allows easy checks:
    # Let (w,v) be current guard ray:
    # - If (w,v) is not in hit_yourself nor in hit_guard, then this is the first occurrence of the
    # ray -> shortest ray -> you can add it, as it does not hit yourself (any future occurrence of
    # this exact same ray, will have first hit the guard).

    # Note: Code could have been more succinctly written, as there are a lot of similarities
    # between the blocks of code for (x>=0, y>=0), (x>=0, y<0) and so on. I nevertheless wrote it
    # like this, as I felt it helped readability.

    # loop x>=0
    x = 0
    while True:
        doneWithPositive = False  # bool indicating when to switch to x<0

        # loop y>=0
        y = 0

        while True:
            # get my position and the guard's position in the 'expanded' mirrored space
            myPosition, guardPosition = getPositions(x, y, dimensions, your_position, guard_position)

            # get my vector and add it in the set
            myVector = positionToVector(your_position,myPosition)
            hit_yourself.add(tuple(myVector))

            # compute euclidean distance squared
            euclidGuard = euclideanDistance(guardPosition, your_position)
            if isCloseEnough(euclidGuard, distance) == False:
                if y == 0:  # we depleted distance on y=0 -> any other y!=0 for x'>=x will be worse -> stop x>=0
                    doneWithPositive = True
                break  # if we are out of distance for y, then we will be out of distance for y+k, k>0 -> break

            # get direction vector to guard
            guardVector = positionToVector(your_position,guardPosition)

            if tuple(guardVector) not in hit_yourself:  # if first occurrence is not hitting us -> add it!
                hit_guard.add(tuple(guardVector))
            y += 1

        if doneWithPositive:
            break

        # loop y<0
        y = -1

        while True:
            # get my position and the guard's position in the 'expanded' mirrored space
            myPosition, guardPosition = getPositions(x, y, dimensions, your_position, guard_position)

            # get my vector and add it in the set
            myVector = positionToVector(your_position,myPosition)
            hit_yourself.add(tuple(myVector))

            # compute euclidean distance squared
            euclidGuard = euclideanDistance(guardPosition, your_position)
            if isCloseEnough(euclidGuard, distance) == False:
                break  # if we are out of distance for y, then we will be out of distance for y-k, k>0 -> break

            # get direction vector to guard
            guardVector = positionToVector(your_position,guardPosition)

            if tuple(guardVector) not in hit_yourself:  # if first occurrence is not hitting us -> add it!
                hit_guard.add(tuple(guardVector))
            y -= 1

        x += 1
    # loop x<0
    x = -1
    while True:
        doneWithNegative = False  # bool indicating when we are done with x<0

        # loop y>=0
        y = 0
        while True:
            # get my position and the guard's position in the 'expanded' mirrored space
            myPosition, guardPosition = getPositions(x, y, dimensions, your_position, guard_position)

            # get my vector and add it in the set
            myVector = positionToVector(your_position, myPosition)
            hit_yourself.add(tuple(myVector))

            # compute euclidean distance squared
            euclidGuard = euclideanDistance(guardPosition, your_position)
            if isCloseEnough(euclidGuard, distance) == False:
                if y == 0:  # we depleted distance on y=0 -> any other y!=0 for x'<=x will be worse -> stop x<0
                    doneWithNegative = True
                break  # if we are out of distance for y, then we will be out of distance for y+k, k>0 -> break

            # get direction vector to guard
            guardVector = positionToVector(your_position, guardPosition)

            if tuple(guardVector) not in hit_yourself:  # if first occurrence is not hitting us -> add it!
                hit_guard.add(tuple(guardVector))
            y += 1
        # loop y<0
        y = -1
        if doneWithNegative:
            break
        while True:
            # get my position and the guard's position in the 'expanded' mirrored space
            myPosition, guardPosition = getPositions(x, y, dimensions, your_position, guard_position)

            # get my vector and add it in the set
            myVector = positionToVector(your_position, myPosition)
            hit_yourself.add(tuple(myVector))

            # compute euclidean distance squared
            euclidGuard = euclideanDistance(guardPosition, your_position)
            if isCloseEnough(euclidGuard, distance) == False:
                break  # if we are out of distance for y, then we will be out of distance for y-k, k>0 -> break

            # get direction vector to guard
            guardVector = positionToVector(your_position, guardPosition)

            if tuple(guardVector) not in hit_yourself:  # if first occurrence is not hitting us -> add it!
                hit_guard.add(tuple(guardVector))

            y -= 1
        x -= 1
    return hit_guard

def sign(x):
    """ Returns the sign of number x."""
    return x/abs(x)

def euclideanDistance(x,y):
    """ Returns euclidean distance squared. """
    return (x[0]-y[0])**2 + (x[1]-y[1])**2

def isCloseEnough(euclideanDistance,distance):
    """ Checks if euclideanDistance <= distance squared """
    return euclideanDistance <= distance ** 2

def getPositions(x,y,dimensions, your_position, guard_position):
    """ Computes positions corresponding to your_position and guard_position in
        the (x,y)-th room (in the expanded space). """
    flipHorizontal = x%2==1  # Flip around y axis
    flipVertical = y%2==1  # Flip around x axis

    # copies
    guardPosition = guard_position[:]
    yourPosition = your_position[:]

    if flipHorizontal:  # flip around y axis
        guardPosition[0] = dimensions[0] - guardPosition[0]
        yourPosition[0] = dimensions[0] - yourPosition[0]

    if flipVertical:  # flip around x axis
        guardPosition[1] = dimensions[1] - guardPosition[1]
        yourPosition[1] = dimensions[1] - yourPosition[1]

    # After applying flips, shift the positions to the (x,y)-th room
    guardPosition[0] += x*dimensions[0]
    guardPosition[1] += y*dimensions[1]
    yourPosition[0] += x * dimensions[0]
    yourPosition[1] += y * dimensions[1]

    return yourPosition, guardPosition


dimensions = [3, 2]
yourLoc = [1, 1]
enemyLoc = [2, 1]
distance = 4
print(solution(dimensions, yourLoc, enemyLoc, distance))


# for dist in range(20):
#     print('for distance', dist)
#     print(solution(dimensions, yourLoc, enemyLoc, dist))
#     print('##################')