n = int(input())
for i in range(n):
    nums = input().split()
    for j in range(len(nums)):
        nums[j] = int(nums[j])
    min = nums[0]
    max = nums[0]
    for num in nums:
        if num < min:
            min = num
        elif num > max:
            max = num
    nums.remove(min)
    nums.remove(max)
    print(nums[0])