def generateDictionary(n=4):
    """ Given n, generate a dictionary d[x] = i such that i = binaryRepresentation(x)
        for all x < n"""
    m = 2**n
    d = dict()
    for i in range(m):
        format = "{0:0"+str(n)+"b}"
        binary = list(format.format(i))
        d[i] = [int(binary[j]) for j in range(len(binary))]

    return d


p = [[True, False, True], [False, True, False], [True, False, True]]

p2 = [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]

p3 = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]



def boolToInt(p):
    """ Convert boolean p[][] to int[][] such that p[i][j] = 1 iff p[i][j]=True, 0
        otherwise. """
    return [[1*p[i][j] for j in range(len(p[0]))] for i in range(len(p))]

def isLegal(prevCol, currentCol,index,g):
    """ We wish to check if column pair (c1,c2) is legal. Given (c1,c2), target grid g and
        index such that (c1,c2) and an "index", this method infers whether (c1,c2) generates
         g[:][index]."""
    height = len(prevCol)  # n+1
    legalColumns = True
    for h in range(1,height):
        if g[h-1][index] == 1:
            if prevCol[h-1] + currentCol[h-1] + prevCol[h] + currentCol[h] != 1:
                legalColumns=False
                break
        else:
            if prevCol[h - 1] + currentCol[h - 1] + prevCol[h] + currentCol[h] == 1:
                legalColumns=False
                break

    return legalColumns

def prevColIsLegal(prevCol,g,index):
    """ Special method, used to evaluate whether column c1 is legal (regardless of c2). More specifically, it returns
        false iff c1[h-1] = c1[h] = 1 (have two 0s) and g[h-1][index] = 1."""
    height = len(prevCol)
    for h in range(1,height):
        # if c1[h-1] = c1[h] = 1 (sum = 2) and g[h-1][index]=1, thn regardless of c2, this column is illegal (we already
        # have too many 0s).
        if g[h-1][index] == 1 and (prevCol[h-1] + prevCol[h]==2):
            return False
    return True


def solution(g):
    """ Solution for expanding nebula problem. Given a grid 'g', finds the total number of grids 'G' which generate 'g'
        after applying said rules. Total time complexity of algorithm for 'g' of size m x n is O(m 4^n). """
    # convert g from bool[][] to int[][]
    g = boolToInt(g)

    # compute dimensions
    height = len(g)
    width = len(g[0])

    # O(m 4^n) complexity -> we want 'n' to be the smallest of the two dimensions. By default m = width and n = height.
    # If n > m (height > width) do the same for the transpose matrix
    if height > width:
        g = [[g[i][j] for i in range(height)] for j in range(width)]  # transpose
        # recalculate dimensions
        height = len(g)
        width = len(g[0])

    # generate dictionary (to iterate through possible columns)
    d = generateDictionary(height+1)

    # count[i][c] = # of solutions for subproblem g[:][:i] with G[:][i]=c
    # As we will see, because count[i+1][c] is based entirely on count[i][c],
    # we can instead only store [i]->0 and [i+1]->1 (memory optimisation).
    count = [[0 for _ in range(len(d))] for _ in range(2)]
    # Initialize count[0] = 1
    count[0] = [1 for _ in range(len(d))]

    for index in range(1,width+1):
        # Check for illegal columns c (regardless of the adjacent columns)
        illegalColumns = dict()
        for cBinary in d.values():
            if not prevColIsLegal(cBinary, g, index-1):
                illegalColumns[tuple(cBinary)] = 1
        for c1, c1Binary in d.items():
            if tuple(c1Binary) in illegalColumns:  # skip illegal columns
                continue
            for c2, c2Binary in d.items():
                if tuple(c2Binary) in illegalColumns:  # skip illegal columns
                    continue
                if isLegal(c1Binary, c2Binary, index-1, g):
                    # (c1,c2) is legal, then count[1][c2] inherits all the solutions of count[0][c1]
                    count[1][c2] += count[0][c1]

        count[0] = count[1][:]  # shift index (count[0] = count[1] and count[1] = np.zeros)
        if index < width:  # no need to set it to zero at the end
            count[1] = [0 for _ in range(len(d))]

    # Solutions = Solutions-Ending-In-c1 + Solutions-Ending-In-c2 + ....
    return sum(count[1])
import time

start = time.time()
print(solution(p))

#gridToBoard(p3)