def average(nums):
    total = 0
    for i in range(1, len(nums)):
        total += nums[i]
    return total / len(nums)


scores = [90, 85, 77]
print("Average:", average(scores))
print("Empty class average:", average([]))
