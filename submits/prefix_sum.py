def make_prefix_array(array):
    result = [0]
    for value in array:
        result.append(result[-1] + value)
    return result

array = list(map(int, input().split()))
prefix_array = make_prefix_array(array)
n = int(input())
for i in range(n):
    from_idx, to_idx = map(int, input().split())
    from_idx, to_idx = from_idx + 1, to_idx + 1
    print(prefix_array[to_idx] - prefix_array[from_idx - 1])
