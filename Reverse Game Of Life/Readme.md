# Reverse Game of Life (Expanding Nebula)

In this problem, we are tasked with analysing a system acting similarly to the famous [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). We are given a grid of 
O and X at time step 't'. At 't+1', the grid shrinks, with each cell inspecting itself, the one below, the one to the right, and the one diagonally below it:
* If the induced box (containing the four aforementioned cells), contains a single X, then grid[i][j][t+1] = X
* Else, grid[i][j][t+1] = O

Given a grid g, we need to find the number of grid predecessors G, such that g = G at the next time step. The grid is m x n, with m, n >= 3, **but** m = width <=50 while n = row <= 10.

Note: I named this problem Reverse Game of Life, because they share similar dynamics (and we need to move backwards in time).

## Example

| | | |
|---|---|---|
|X|O|X|
|O|X|O|
|X|O|X|

can derive from 


| | | | | 
|---|---|---| ---|
|O|X|O|O| 
|O|O|X|O|
|O|O|O|X|
|X|O|O|O|

| | | | | 
|---|---|---| ---|
|O|O|X|O| 
|O|X|O|O|
|X|O|O|O|
|O|O|O|X|

| | | | | 
|---|---|---| ---|
|X|O|O|O| 
|O|O|O|X|
|O|O|X|O|
|O|X|O|O|

| | | | | 
|---|---|---| ---|
|O|O|O|X| 
|X|O|O|O|
|O|X|O|O|
|O|O|X|O|

Result = 4

## Solution

This is a difficult problem (resembles sudoku which is known to be NP complete), and as such I will make use of the assymetry between the max number of rows and the max number of 
columns. The algorithm (its core) works as follows:
1. Given m x n grid 'g', make it so n <= m (transpose if needed)
1. Generate all possible columns. As the rows are at most 10, we have at most 2<sup>10</sup> such columns
1. Consider matrix count[i][c] = number of solutions for subproblem g[:][:i] with G[:][i] = c (ending with column 'c')
1. Populate this matrix bottom up, initializing count[0][c] = 1 for all c
1. For i > 0, for every pair of **legal** columns (c1,c2) (simple O(1) check), count[i+1][c2] += count[i][c1] 
1. Return the sum of the final column: total generating grids G = generating grids ending in c1 + generating grids ending in c2 + ...

Note that I have also further optimised the code:
* Memory wise, by noticing that once we compute check[i], then we can discard check[i-1] (never reused).
* Time wise, by applying further checks (in special cases) to avoid redudant column checking (c1,c2) (see code for more details).

Final time complexity is O(m 4<sup>n</sup>), as we iterate m times (i = 0 to m-1), and in each iteration we check every possible pair (c1,c2) (4<sup>n</sup>). Because n is at most 10,
the exponent is 'handable'. Note that it is cruical to make sure n <= m as n is located at the exponent.
