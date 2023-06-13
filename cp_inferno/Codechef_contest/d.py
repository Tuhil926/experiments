T = int(input())
for i in range(T):
    A = [int(x) for x in input().split()]
    N = A[0]
    p1 = [A[1], A[2]]
    p2 = [A[3], A[4]]
    dist_inside = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    dist_outside = min([p1[0], p1[1], N - p1[0] + 1, N - p1[1] + 1]) + min([p2[0] + p2[1], N - p2[0] + 1, N - p2[1] + 1])
    min_cost = min((dist_outside, dist_inside))
    print(min_cost)
