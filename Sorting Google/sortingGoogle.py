def solution(l):
    """ Given a list 'l' of elevator IDs, returns the corresponding sorted list."""
    # We simply need to perform a merge sort (O(nlogn))
    # with a custom string comparator
    return mergeSort(l, 0, len(l) - 1)


def compareElevator(elevator1, elevator2):
    """ Custom String Comparator. """
    sequence1 = elevator1.split('.')
    sequence2 = elevator2.split('.')
    minSequence = min(len(sequence1), len(sequence2))
    result = 0
    for i in range(minSequence):
        if int(sequence1[i]) < int(sequence2[i]):
            result = -1
            break
        if int(sequence1[i]) > int(sequence2[i]):
            result = 1
            break

    # If their common subsquence is equal, check size
    if result == 0:
        if len(sequence1) > len(sequence2):
            result = 1
        elif len(sequence1) < len(sequence2):
            result = -1
    return result


def mergeSort(elevatorList, start, finish):
    """ Custom implementation of traditional merge sort (Based on custom string comparator)"""
    half = int((finish + start) / 2)
    # recursion base
    if start == finish:
        return [elevatorList[start]]
    elif finish == start + 1:
        elevatorList1 = [elevatorList[start]]
        elevatorList2 = [elevatorList[finish]]
        return sortSortedArrays(elevatorList1, elevatorList2)
    # recursion
    else:
        elevatorList1 = mergeSort(elevatorList, start, half)
        elevatorList2 = mergeSort(elevatorList, half + 1, finish)

        return sortSortedArrays(elevatorList1, elevatorList2)


def sortSortedArrays(elevatorList1, elevatorList2):
    """ Handy method that merges two sorted arrays into one. """
    # It is easy to sort two sorted arrays (linear)
    sortedList = []
    while max(len(elevatorList1), len(elevatorList2)) > 0:
        if len(elevatorList1) == 0:
            sortedList = sortedList + elevatorList2
            elevatorList2 = []
        elif len(elevatorList2) == 0:
            sortedList = sortedList + elevatorList1
            elevatorList1 = []
        elif compareElevator(elevatorList1[0], elevatorList2[0]) < 0:
            element = elevatorList1.pop(0)
            sortedList.append(element)
        else:
            element = elevatorList2.pop(0)
            sortedList.append(element)

    return sortedList


list = ['1.1.2','1.0','1.3.3', '1.0.12','1.0.2']

print(solution(list))
