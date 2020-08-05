# Sorting Google
In this problem, we are tasked with ordering a list 'l' of strings of a specific format. Each string 'x' is of the format x = a, or x = a.b and so on, where a, b are
natural numbers. 

Examples: 
* x = "10"
* x = "13.1"
* x = "3.12.3"

Sorting is done by comparing strings of this form in a lexicographic manner. For instance:
* "10.2" > "1.31" because 10>1
* "10.2" > "10" since |"10.2"| = 2 > |"10"| = 1 (size comparison)

## Example

l = ['1.1.2','1.0','1.3.3', '1.0.12','1.0.2'] -> sorted: ['1.0', '1.0.2', '1.0.12', '1.1.2', '1.3.3']

## Solution

Sorting based on the Merge Sort algorithm (O(nlogn)), utilising a custom string comparator.
