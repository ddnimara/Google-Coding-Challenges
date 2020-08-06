example = [[0,1,1,1,1,1,1],[1,0,1,1,1,1,1],[1,1,0,1,1,1,1],[1,1,1,0,1,1,1],[1,1,1,1,0,1,1],[1,1,1,1,1,0,1],[-2,1,1,1,1,1,0]]

example2 = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
import math

def bellmanFord(root,matrix):
    """ Bellman-Ford implementation (minimum path in graph with negative edge weights). Given root (start node) and
        transition matrix, returns a 'distance' list (every node's min distance to the root), a 'path' list
        (the corresponding path) and a boolean indicating whether a negative cycle exists."""
    it = 0
    path=dict()
    distance=[math.inf for x in range(len(matrix))]
    distance[root] = 0
    path[root] = [root]
    prevDist = None
    negativeCycle=False
    visited = [root]
    while prevDist!=distance:
        it +=1
        prevDist = distance[:]
        for i in visited:
            for j in range(len(matrix)):
                if j==i:
                    continue
                dist = distance[i] + matrix[i][j]
                if dist <= distance[j]:
                    if dist == distance[j]:
                        if len(path[j]) < len(path[i] + [j]):
                            distance[j] = dist
                            path[j] = path[i] + [j]

                    else:
                        distance[j] = dist
                        path[j] = path[i]+[j]

                if j not in visited:
                    visited.append(j)

            if it >= len(matrix):
                negativeCycle=True
                break
    for i in path.keys():
       path[i] = list(set(path[i]))
    return distance, path, negativeCycle

def bellmanForEach(matrix):
    """ Method which runs bellman ford for each node.
        Returns distance and path lists for each node and a boolean indicating the existence of a negative cycle."""
    distances=[]
    paths=[]
    negativeCycle=False
    for i in range(len(matrix)):
        if negativeCycle==True:
            break
        dist, pat, negativeCycle = bellmanFord(i,matrix)
        distances.append(dist)
        paths.append(pat)

    return distances, paths, negativeCycle


def recursion(matrix, distances, paths, time, position, visited):
    """ Recursively traverse the graph, respecting your remaining time while keeping track of the paths
        traversed thus far and nodes visited. """
    # First, check if we have been here before
    if position not in visited:
        visited.append(position)

    # See what's left
    leftToGo = list(set(range(len(matrix))) - set(visited))

    # Always consider the 'exit'
    if len(matrix)-1 not in leftToGo:
        leftToGo.append(len(matrix)-1)

    results = [position]

    previouslyVisited = visited[:]

    for i in leftToGo:
        if i == position:  # No reason stay in place
            continue
        if time - distances[position][i] - distances[i][-1] >= 0:  # if we have enough time to exit after we go to 'i' place
            path = paths[position][i]
            tempVisited = previouslyVisited[:]
            # update all the nodes you visit along the way
            for locations in path:
                if locations not in previouslyVisited:
                    tempVisited.append(locations)
            # do the same from this point forward with the time that's left after going there
            recurs = recursion(matrix, distances, paths, time - distances[position][i], i, tempVisited)
            # store all the nodes found along the way
            added = path+recurs
            results = results + [added]
    return results

def recursionToList(r):
    """ Process result from the recursion method to a more manageable list. The recursion result contained paths, with nodes
        - location appearing more than once. This method filters excess info."""
    result = []
    index = 0
    if len(r) == 1:
        return [r]
    for i in range(1, len(r)):
        try:
            len(r[i])
        except:
            index = index+1
            continue
        recurs = recursionToList(r[i])
        if len(recurs) == 0:
            temp = r[:index + 1]
            result.append(list(set(temp)))
        else:
            for l in recurs:
                temp = r[:index+1]
                temp = temp + l
                result.append(list(set(temp)))

    return result
def compareBunnies(bunnieList1, bunnieList2):
    """ Bunny comparison. Bunny lists are compared based on their size. Equal size bunnies are ranked
        based on the indeces of their bunnies. """
    # Custom String Comparator
    result = 0
    if len(bunnieList1) > len(bunnieList2):
        return 1
    elif len(bunnieList1) < len(bunnieList2):
        return -1

    for i in range(len(bunnieList1)):
        if bunnieList1[i] < bunnieList2[i]:
            return 1
        if bunnieList1[i] > bunnieList2[i]:
            return -1

    return 0


def solution(matrix,time):
    """ Solution to the bunny problem. Given a Matrix (such that matrix[i][j] = time spent to go from i to j) and a
        max time 'time', returns the max number of bunnies that can be saved within this time frame."""

    # Main idea for problem:
    # - Run bellman ford for each position to compute a distance matrix, giving us min distance from i to j for every (i,j)
    # - Store corresponding minimum paths
    # - If we have negative cycle, then we can save all the bunnies
    # - If not, explore the graph (depending on the time you have), visiting as many nodes as possible and store the paths
    # - Compare all of them and choose the one which saves the most bunnies

    # Run bellman ford from each position
    distances, paths, negativeCycle = bellmanForEach(matrix)
    if negativeCycle:  # If there is a negative cycle, we can exploit it to save all the bunnies
        return [i-1 for i in range(1,len(matrix)-1)]
    # Find all possible paths we can take given our time
    r = recursion(matrix, distances, paths, time, 0, [])
    # Filter it into lists of bunnies (output postprocessing)
    lists = recursionToList(r)
    # Filter out repeated states
    unique = [list(set(lists[i])) for i in range(len(lists))]
    bunnies = []
    for l in unique:
        if 0 in l:  # there are no bunnies at position 0
            l.remove(0)
        if len(matrix)-1 in l:  # last index corresponds to the exit, not any bunnies
            l.remove(len(matrix)-1)
        for number in range(len(l)):  # Position 1 -> bunny 0, Position 2 -> bunny 1 and so on
            l[number] -= 1
        bunnies.append(l)

    # Find best bunny combination based on our comparator (size + indices)
    best = bunnies[0]

    for bunny in range(1, len(bunnies)):
        if compareBunnies(best, bunnies[bunny]) < 0:  # if our best is worse
            best = bunnies[bunny]  # we found a better one

    return best

sol = solution(example2,2)

print('solution',sol)

