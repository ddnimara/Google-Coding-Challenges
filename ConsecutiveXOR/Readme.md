# Consecutive XOR
This problem tasks us with efficiently computing the XOR of natural numbers from a given matrix. 
More specifically, we are given a length by length matrix, filled with consecutive elements, starting with 'x'. We are tasked with 
XORing the elements of the matrix[i][j] for j<length-i.

## Example
x = 17, length = 4:
| | | | |
|---| --- | --- | ---|
| 17 | 18 | 19 | 20 |
| 21 | 22 | 23 | -- |
| 25 | 26 | -- | -- |
| 29 | - | - | -- |

Result: 14

## Solution

The simplest solution would be to simply iterate through the matrix and xor its elements. This would have time complexity (assuming O(1) per XOR) O(length<sup>2</sup>). 
We can do better however, if we use the fact that if x is even, then x ^ (x+1) = 1. We can thus group each row x^(x+1)^(x+2)^(x+3)^...^(x+length-1) adequately:
* If x and length are even, then x^(x+1)^(x+2)^(x+3)^...^(x+length-1) = [x^(x+1)]^[(x+2)^(x+3)]^...^[(x+length-2)^(x+length-1)] = 1^1^1...^1 (# length/2 times) = 
length/2 mod2 
* If x is even and length is odd, then x^(x+1)^(x+2)^(x+3)^...^(x+length-1) = [x^(x+1)^(x+2)^(x+3)^...^(x+length-2)]^(x+length-1). Since length - 1 is even, we can compute the 
first part as before, and do a single xor at the end
* If x is odd, then x+1 is even and thus x^(x+1)^(x+2)^(x+3)^...^(x+length-1) = x^[(x+1)^(x+2)^(x+3)^...^(x+length-1)]. 

Since each row is computed in O(1), this reduces time complexity to O(length)
