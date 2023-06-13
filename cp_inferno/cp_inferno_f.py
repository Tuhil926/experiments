number_of_cases = int(input())
ans = 0
for i in range(number_of_cases):
    ans = 0
    numbers = input().split()
    n = int(numbers[2])
    numbers = [int(numbers[0]), int(numbers[1])]
    if numbers[0] > numbers[1]:
        while numbers[0] <= n and numbers[1] <= n:
            ans += 1
            numbers[ans % 2] += numbers[1 - ans % 2]
    else:
        while numbers[0] <= n and numbers[1] <= n:
            ans += 1
            numbers[1 - ans % 2] += numbers[ans % 2]

    print(ans)