def tournament_sort(arr):
    comparisons = 0
    cache = {}

    def compare(a, b):
        nonlocal comparisons
        if a is None:
            return b
        if b is None:
            return a
        pair = (a, b) if a < b else (b, a)
        if pair in cache:
            return cache[pair]
        print(f"What is greater, 1: {a} or 2: {b}?")
        choice = input()
        winner = a if choice == '1' else b
        cache[pair] = winner
        comparisons += 1
        return winner

    def tournament(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = tournament(arr[:mid])
        right = tournament(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        while left or right:
            if not left:
                result.append(right.pop(0))
                continue
            if not right:
                result.append(left.pop(0))
                continue
            winner = compare(left[0], right[0])
            if winner == left[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        return result

    sorted_arr = tournament(arr)
    print(f"Number of computations: {comparisons}")
    return sorted_arr

# Example usage
# my_list = ["ASTROTHUNDER", "STOP TRYING TO BE GOD", "STARGAZING", "SKELETONS", "CAROUSEL", "NC-17", "YOSEMITE", "WHO? WHAT!", "BUTTERFLY EFFECT", "HOUSTONFORNICATION", "COFFEE BEAN"]
my_list = ["ASTROTHUNDER", "STOP TRYING TO BE GOD", "STARGAZING", "SKELETONS"]
sorted_list = tournament_sort(my_list)
print(sorted_list)
