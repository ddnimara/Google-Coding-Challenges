# Staircase

This problem tasks us with finding all possible staircases comprised of 'n' bricks. A staircase is simply a collection of bricks [x1, x2, x3, ..., xm] such that 
x1 + x2 + ... + xm = n and x1 < x2 < ... < xm. This is equivalent to finding the number of ways n can be partitioned into a sum of **distinct** natural numbers.

## Example

n=3: 

b

bb

Solution: 1

n=5:

b

bbbb

or

bb

bbb

Solution: 2

## Solution

We utilise dynamic programming, by considering the matrix 'm' such that m[i][j] refers to how many ways I can write i = j + ... with j: largest number.
For instance, m[3][2] = 1 since there is only one way to write 3 = 2 + ... (1). Similarly, m[10][4]= 1 since there is one way to write 10 = 4 + 3 + 2 + 1. 
We can then simply build our way bottom up, computing m[i][j] either directly (in some edge cases), or via m[i][l], l < j. For example, 10 = 9 + 1 = 8 + 2 = 7 + 3 = 
6 + 4 = 6 + 3 + 1 = 5 + 4 + 1 = 5 + 3 + 2 = 4 + 3 + 2 + 1. Note that 5 + 4 + 1 = 5 + 3 + 2 can be found via m[5], as we have 5 + ways to break down (10-5). 
