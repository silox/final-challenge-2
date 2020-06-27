def binary_search(arr, val):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == val:
            return mid
        elif val < arr[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return -1


input_array = list(map(int, input().split()))
for value in map(int, input().split()):
    print(binary_search(input_array, value))
