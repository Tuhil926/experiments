n = int(input())
for i in range(n):
    n, c, d = [int(x) for x in input().split()]
    rewards = [int(x) for x in input().split()]
    rewards.sort(reverse=True)
    