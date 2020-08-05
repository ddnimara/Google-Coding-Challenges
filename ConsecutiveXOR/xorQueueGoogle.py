def rowSolution(start, length):
    """ Given an initial number start and a length, returns the XOR that corresponds to the consecutive numbers
        start, start + 1, ..., start + (length-1). """

    # The gist of this problem lies in the simple observation that if x is even, then x^(x+1) = 1 (^ -> xor)
    # Thus, we simply group our start, start + 1, ... in such pairs of (x,x+1) such that x is even.
    if start % 2 == 0:
        if length % 2 == 0:  # xor of (x,x+1,..., x+length-1) = [x^(x+1)]^[(x+2)^(x+3)]^...
            return int(length/2) % 2
        else:  # xor of (x,x+1,..., x+length-1) = xor of (x,x+1,..., x+length-2) ^ (start + length - 1)
            return int((length-1)/2) % 2 ^ (start+length-1)
    else:  # xor of (x,x+1,..., x+length-1) = x ^ xor of (x+1,..., x+length-1)
        return start ^ rowSolution(start+1, length-1)

def solution(start, length):
    """ Given a number 'start' and a given length, considers the length x length matrix containing consecutive numbers
        start, start + 1, ..., start + length * length, and efficiently returns their xor (O(length))."""
    # Compute the xor of the first Row in O(1)
    res = rowSolution(start, length)
    print('start',start)
    # Loop through the rest of the rows
    for i in range(1, length):
        # Each row's XOR is computed in O(1) and is added to the thus far computed XOR
        start = start + length
        print('start', start)
        res = res ^ rowSolution(start, length-i)
    return res


print(solution(17,4))

