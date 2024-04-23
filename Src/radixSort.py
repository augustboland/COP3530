def radix_sort(arr):
    # Helper function to perform counting sort
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        # Store count of occurrences in count[]
        for i in range(n):
            index = abs(arr[i]) // exp
            count[int(index % 10)] += 1

        # Change count[i] so that count[i] now contains actual position of this digit in output[]
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array using the modified count[]
        i = n - 1
        while i >= 0:
            index = abs(arr[i]) // exp
            output[count[int(index % 10)] - 1] = arr[i]
            count[int(index % 10)] -= 1
            i -= 1

        # Copy the output array to arr[], so that arr now contains sorted numbers
        for i in range(n):
            arr[i] = output[i]

    # Determine the maximum number to decide the number of digits
    max1 = max(abs(x) for x in arr)

    # Handle negative numbers by offsetting with the minimum value
    min1 = min(arr)
    offset = -min1 if min1 < 0 else 0
    arr = [x + offset for x in arr]

    # Apply counting sort to sort elements based on place value.
    exp = 1
    while max1 // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr
    # Reverse the offset for negative numbers
    if offset:
        arr = [x - offset for x in arr]