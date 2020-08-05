example1 = [[0,1,0,0,0,1],[4,0,0,3,2,0], [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

example2 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]
example3 = [[2,1,2,0,0,0,1],[3,0,0,1,1,0,0],[0,0,1,1,0,0,0],[0,0,1,3,0,0,0],[0,0,0,0,0,1,0],[0,0,0,0,0,1,3],[0,0,0,0,1,0,1]]
from fractions import Fraction

example4 = [[1,1,0,0],[1,4,1,0],[1,0,1,1],[0,0,0,0]]
import math

def normalize(matrix):
    """ Given a matrix M, normalizes it to be row stochastic"""
    for i in range(len(matrix)):
        eta = sum(matrix[i])
        if eta>0:
            for j in range(len(matrix[0])):
                matrix[i][j] = Fraction(matrix[i][j],eta)
        elif eta==0 or matrix[i][i]==1:
            matrix[i][i] = 1
    return matrix

def lcm(a, b):
    """ Returns LCM of (a,b)"""
    #gcd*lcm=a*b
    return abs(a*b) // math.gcd(a, b)

def lcmOfList(list):
    """ Used to convert the final fractions to numerators / common denominator """
    if len(list)==1:
        return list[0]
    result = lcm(list[0],list[1])

    for i in range(1,len(list)):
        result = lcm(result,list[i])
    return result

def luDecomposition(matrix,b):
    """ Solving matrix * x  = b via LU decomposition"""
    # copy
    a=[matrix[i][:] for i in range(len(matrix))]
    n = len(b)
    x = [0]*n
    y = [0]*n
    # a[i][j] = L + U - I
    # Normally, you use two separate matrices, L and U
    # Use one for memory saving (uper part is U, lower part is L)
    for i in range(0,n):
        for j in range(0,i):
            alpha = a[i][j]
            for k in range(0,j):
                alpha = alpha - a[i][k]*a[k][j]
            a[i][j] = alpha/a[j][j]
        for j in range(i,n):
            alpha = a[i][j]
            for k in range(0,i):
                alpha = alpha - a[i][k]*a[k][j]
            a[i][j] = alpha
    # After you have A = LU, then Ax = b -> Ux = y, Ly = b. Due to their nature,
    # these two systems are easily solved via forward and backwards pass.
    # Ly = b
    for i in range(n):
        alpha = 0
        for k in range(i+1):
            alpha = alpha + a[i][k]*y[k]
        y[i] = b[i] - alpha
    # Ux = y
    for i in range(n-1,-1,-1):
        alpha = 0
        for k in range(i+1,n):
            alpha = alpha + a[i][k]*x[k]
        x[i] = (y[i] - alpha)/a[i][i]
    return x

def fractionToSolution(fractions):
    """ Returns numerator of fractions with common denominator + their common denominator at the end.
        For instance, [1/3,2/9, 4/9] -> [3, 2, 4, 9]. """
    numerators = [fractions[i].numerator for i in range(len(fractions))]
    denominator = [fractions[i].denominator for i in range(len(fractions))]
    lcm = lcmOfList(denominator)
    result = [(numerators[i] * Fraction(lcm,denominator[i])).numerator for i in range(len(fractions))]
    result.append(sum(result))
    return result


def bfs(matrix,root):
    """ Traditional BFS implementation"""
    visited = [0 for i in range(len(matrix))] # visited[i] = 0 iff there is no path from root->i
    queue = [root]
    #visited[root]=1
    while len(queue)>0:
        parent = queue.pop(0)
        for i in range(len(matrix)):
            if matrix[parent][i]!=0 and visited[i]==0:
                queue.append(i)
                visited[i]=1

    return visited


def findStronglyConnectedComponents(matrix):
    """ Method used to find the strongly connected components of the graph induced by the markov matrix.
        Returns a list with the strongly connected components (clusters) and a Path Matrix (pathMatrix[i][j]==1 iff
        there exists a path from state i to state j). """
    pathMatrix = []
    for i in range(len(matrix)):
        pathMatrix.append(bfs(matrix, i))

    components = []

    alreadyBelongs = [0]*len(matrix)
    for i in range(len(matrix)):
        if alreadyBelongs[i] > 0:
            continue
        if pathMatrix[i][i] > 0:
            temp_component = [i]
            alreadyBelongs[i] = 1
        else:
            temp_component=[]
        for j in range(i+1,len(matrix)):
            if pathMatrix[i] == pathMatrix[j]:
                if len(temp_component) == 0:
                    temp_component.append(i)
                    alreadyBelongs[i] = 1
                temp_component.append(j)

                alreadyBelongs[j]=1

        components.append(temp_component)
    return components, pathMatrix


def findTerminalStates(stronglyConnectedComponents, pathMatrix):
    """ Method that locates Terminal States, given our strongly connected Components
        and our Path Matrix.
        Returns terminal states + a bool indicating whether or not our initial state
        is a terminal state. """
    terminalStates = []
    initialStateIsTerminal=False
    for component in stronglyConnectedComponents:
        if len(component) > 0 and len(component) == sum(pathMatrix[component[0]]):
            terminalStates.append(component)
            if 0 in component:
                initialStateIsTerminal=True
    return terminalStates, initialStateIsTerminal

def generateMatrix(matrix,terminalStates):
    """ Given markov matrix M and a list of terminal states, generates the corresponding matrix
        required in the analytical system (see defineAnalyticalSystem).
        Returns M', b which define the aforementioned system M'x = b. """
    newMatrix = [[0 for x in range(len(terminalStates)-1)] for y in range(len(terminalStates)-1)]
    b = [0 for x in range(len(terminalStates) - 1)]
    # set p0 = 1, we normalize later
    for i in range(1,len(terminalStates)):
        for j in range(1,len(terminalStates)):
            newMatrix[j-1][i-1] = 1*(i==j) - matrix[terminalStates[i]][terminalStates[j]]
        b[i-1] = -matrix[terminalStates[0]][terminalStates[i]]
    return newMatrix,b

def classSolution(solution):
    """ Returns the within class probabilities. """
    result = [1]  # Recall we set p0 = 1.
    result = result + [abs(solution[i]) for i in range(len(solution))]
    result = fractionToSolution(result)
    return result

def solutionToFraction(sol):
    """ Given solutions [x1,x2,...,xn,a] returns the corresponding probabilities [x1/a, x2/a, ..., xn/a]"""
    result = [Fraction(sol[i],sol[-1]) for i in range(len(sol)-1)]
    return result


def defineAnalyticalSystem(matrix, junkStates):
    """ Given our Markov matrix M and a set of terminal states (junkstates), this method
        defines a set of analytical systems (I-M) x = b_i that need to be solved in order to
        find the underlying probabilities.
        Returns I-M matrix as well as a list containing the b_i."""
    # This is the core of this solution.
    # Essentially, let P_i,j be the probability of ending up at state j (terminal state)
    # from state i. We are interested in P_1,j for every terminal state.
    # For instance, lets assume we wanna compute P_1,4 (where 4 is one of the terminal states).
    # Then from 1, we can either go at state 2 or at state 5. Also, from state 2 we can go back
    # to state 1 or state 4 or 5. Thus, P_1,4 = 1/2 P_2,4 + 1/2 P_5,4 and P_2,4 = 4/9 P_1,4 + 3/9 P_4,4 + 2/9 P_4,5
    # Note, however, that P_5,4 = P_4,5 = 0 (terminal states other than 4) and P_4,4 =1. This generates a linear equation
    # Ax = b which we have to solve.
    result = []
    terminalStates= []
    for i,terminal in enumerate(junkStates):
        terminalStates = terminalStates + terminal

    nonJunkStates = list(set(range(len(matrix))) - set(terminalStates))
    beta = [[0 for x in range(len(nonJunkStates))] for y in range(len(junkStates))]
    # We have len(JunkStates) number of betas, one for each junkState. A remains the same.
    for index_i,i in enumerate(nonJunkStates):
        row = []
        for k in nonJunkStates:
            row.append(1*(k==i) - matrix[i][k])
        for index,junk in enumerate(junkStates):
            sum=0
            for k in range(len(junk)):
                sum += matrix[i][junk[k]]
            beta[index][index_i]=sum
        result.append(row)

    return result, beta



def solution(m):
    """ Given a matrix 'm' describing the probabilities of transitioning from state i to state j,
        returns a list [x1,x2, ..., xn, a] such that p_i = x_i/a describes the probability of ending up
        at the i-th terminal state. """
    # Make matrix m row stochastic
    markovMatrix = normalize(m)
    # Find its strongly connected components
    stronglyConnectedComponents, pathMatrix = findStronglyConnectedComponents(markovMatrix)
    # Find its terminal states
    terminalStates, startIsTerminal = findTerminalStates(stronglyConnectedComponents, pathMatrix)
    withinComponentProbabilities = []
    for terminalState in terminalStates:
        if len(terminalState) == 1:
            withinComponentProbabilities.append(1)
        else:  # solve linear system within that class
            matrixWithinComponent, b = generateMatrix(markovMatrix, terminalState)
            solution = luDecomposition(matrixWithinComponent, b)
            fract = classSolution(solution)
            result = solutionToFraction(fract)
            withinComponentProbabilities.append(result)

    if startIsTerminal == False:
        a, b = defineAnalyticalSystem(markovMatrix, terminalStates)
        fractions = [luDecomposition(a, b[i])[0] for i in range(len(b))]
        classProbabilities = fractionToSolution(fractions)
        classProbabilities = solutionToFraction(classProbabilities)
    else:  # Only s0 class is reachable as s0 is terminal
        fractions = []
        for index,terminalState in enumerate(terminalStates):
            if index == 0:  # probability = within class probability
                if len(terminalState) == 1:
                    fractions.append(withinComponentProbabilities[0])
                else:
                    fractions.append(withinComponentProbabilities[0][index])
            else:
                for _ in terminalState:
                    fractions.append(0)  # Unreachable
        classProbabilities = fractionToSolution(fractions)
        classProbabilities = solutionToFraction(classProbabilities)
    # final preprocessing of probabilities to obtain desired form
    finalFractions = []
    for i in range(len(terminalStates)):
        if len(terminalStates[i])==1:
            finalFractions.append(classProbabilities[i])
        else:
            for j in range(len(terminalStates[i])):
                finalFractions.append(withinComponentProbabilities[i][j] * classProbabilities[i])

    return fractionToSolution(finalFractions)



print(solution(example1))

