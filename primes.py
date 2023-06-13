import time

n = 100000
primes = [2]
start_time = time.time_ns()
for i in range(2, n):
    for j in range(len(primes)):
        if i % primes[j] == 0:
            break
    else:
        primes.append(i)
end_time = time.time_ns()
print(primes)
print("Time taken: ", (end_time - start_time)/1000000000)

n = 100000
primes = [2]
start_time = time.time_ns()
j, k = 0, 0
for i in range(2, n):
    j = 0
    k = i**0.5
    while primes[j] <= k:
        j += 1
        if i % primes[j] == 0:
            break
    else:
        primes.append(i)
end_time = time.time_ns()
primes.remove(2)
print(primes)
print("Time taken: ", (end_time - start_time)/1000000000)
