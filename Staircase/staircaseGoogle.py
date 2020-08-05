import math

def solution(n):
    """ Solution to the Staircase Problem: Given a number 'n', returns the number of staircases comporised of 'n' bricks.
        This is equivalent to finding the number of ways n can be partitioned into a sum of DISTINCT natural numbers. """
    # if I have matrix m, then the result for
    # n is the sum m[n][i], for 1<=i<n
    if n < 5:
        return 1
    m = generateMatrix(n)
    result = 0
    for i in range(n):
        result += m[n][i]

    return result


def generateMatrix(n):
    # m[i][j] refers to how many ways can I
    # write i = j + ... with j: largest number
    # Example m[3][2] = 1 since there is only
    # one way to write 3 = 2 + ... (1)
    # Similarly, m[10][4]= 1 since there is one way
    # 10 = 4 + 3 + 2 + 1
    m = [[0 for x in range(n + 1)] for y in range(n + 1)]
    m[3][2] = 1
    m[4][3] = 1
    for i in range(5, n + 1):
        for j in range(3, i):
            k = math.ceil(i/2)
            if j > i - k:
                m[i][j] = 1

            for l in range(1, j):
                m[i][j] += m[i - j][l]
    return m


print(solution(10))
