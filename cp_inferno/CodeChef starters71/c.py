T = int(input())

for i in range(T):
    streak = 0
    temp_streak = 0
    N = int(input())
    A = [int(x) for x in input().split()]
    B = [int(x) for x in input().split()]
    for j in range(N):
        if A[j] == 0 or B[j] == 0:
            if streak < temp_streak:
                streak = temp_streak
            temp_streak = 0
        else:
            temp_streak += 1
    if streak < temp_streak:
        streak = temp_streak
    print(streak)