# Algebra Systems 

Let us consider all the n x m grids such that each cell contains a number betwee 1 and s (inclusive). We wish to find all the possible grid configurations under the collumn and row
symmetry. That is, grids a and b are equivalent, if we can form b, by applying row and column swaps on a.

## Example
n = m = s = 2
| |
|---|
|11|
|11|

| | | | |
|---|---|---|---|
|21| 12| 11| 11|
|11|11|21|12|

| | |
|---|---|
|22| 11|
|11|22|

| | |
|---|---|
|12| 21|
|12|21|

| | |
|---|---|
|12| 21|
|21|12|

| | | | |
|---|---|---|---|
|12| 21| 22| 22|
|22|22|21|12|

| |
|---|
|22|
|22|

Result = 7

# Solution

This problem borrows heavily from Group Theory (Algebra). In fact, we have a set X of elements (all possible n x m grids with cells containing numbers from 1 to s) on which we 
apply a symmetry group G. We wish to find all the [orbits](https://en.wikipedia.org/wiki/Group_action#Orbits_and_stabilizers). In my solution, I use [Burnside's Lemma](https://en.wikipedia.org/wiki/Burnside%27s_lemma)
to enumerate said orbits (see code for more information).
