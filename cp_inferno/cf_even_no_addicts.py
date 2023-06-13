for i in range(int(input())):
    n = int(input())
    a = [int(x) for x in input().split()]
    no_even = 0
    for num in a:
        if num % 2 == 0:
            no_even += 1
    no_odd = n - no_even
    if no_even % 2 == 1:
        if no_odd % 2 == 1:
            if (no_odd - int(no_odd / 2)) % 2 == 0:
                print("Alice")
            else:
                print("Alice")
        else:
            if int(no_odd / 2) % 2 == 0:
                print("Alice")
            else:
                print("Bob")
    else:
        if no_odd % 2 == 0:
            if int(no_odd / 2) % 2 == 0:
                print("Alice")
            else:
                print("Bob")
        else:
            if (no_odd - int(no_odd / 2)) % 2 == 0:
                print("Alice")
            else:
                print("Bob")