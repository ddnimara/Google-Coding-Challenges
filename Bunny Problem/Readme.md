# Bunny Problem

Suppose we have a matrix m[i][j], such that m[i][j] = time spent on going from point i to point j. First and last columns correspond to the start and exit respectively. All other
collumns contain a bunny. We are tasked with saving as many bunnies as possible (visiting as many points) within a limiting time. Note that m[i][j] can be negative (gain time). Note that we must reach the exit on non negative time.


## Example

|start|bunny 0|bunny 1|bunny 2| exit|
|---|---|---|---|---|
|0|2|2|2|-1|
|9|0|2|2|-1|
|9|3|0|2|-1|
|9|3|2|0|-1|
|9|3|2|2|0|

Time = 3s

Result = [0,1,2] (saved all bunnies)

Examplary path: start (3s)-> bunny 0 (1s)-> exit (2s)-> bunny 1 (0s) -> exit (1s) -> bunny 2 (-1s) -> exit (0s)

## Solution

We essentially need to traverse a graph (which can also contain megative edges), visiting as many nodes as we possibly can, before exiting the graph (ending up
at its last column), within the given time frame. My approach can be summarized as follows:
1. Run bellman ford for each position to compute a distance matrix, giving us min distance from i to j for every (i,j)
1. Store corresponding minimum paths
1. If we have negative cycle, then we can save all the bunnies (use it to get as much time as needed)
1. If not, explore the graph (depending on the time you have), visiting as many nodes as possible and store the paths
1. Compare all of them and choose the one which saves the most bunnies (based on number of bunnies saved and their indices)
