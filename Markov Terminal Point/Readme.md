# Markov Terminal Point

This problem tasks us with finding the probability of (eventually) ending up at a stable point-state, given an initial state s0. State transitions follow the markovian property,
that is our state at time t depends only on our state at t-1. We are given the markovian matrix M', populated with the corresponding transitions, which corresponds 
in the most natural way to the markovian matrix M[i][j] = p[s(t) = j | s(t-1) = i] = rowNormalize(M'[i][j]).
The result must have a specific format [x1, x2, x3, ..., xn, a], such that p1 = x1/a, ... pn = xn/a, pi: the probability of the i-th stable state.

## Example
[4,0,0,3,2,0], [0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

| s0      | s1 | s2 | s3 | s4 |s5| 
| :---       |    :----:   | :---:|:---:|:---:|          ---: |
| 0    | 1     |  0 |  0| 0 | 1 
| 4   | 0       | 0| 3|2 |0|
|0 |0|0|0|0|0|
|0 |0|0|0|0|0|
|0 |0|0|0|0|0|

Result : [0, 3, 2, 9, 14]

## Solution 

Without going into too much technical details (See code for more information), my solution works as follows:
1. Convert M' to the corresponding Markovian Matrix M.
1. Find Strongly Connected Components of the corresponding Graph. Each such component represents a class.
1. Find the probabilities P[reach Class i | s0]. 
1. For each reachable class, find the P[terminal state j | Class i].
1. P[terminal state j| s0 ]  = P[reach Class i | s0] * P[terminal state j | Class i].
1. Output result in the desired format.
