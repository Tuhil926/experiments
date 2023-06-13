import random
import time
numbers = []
number_of_elements = 100000
max_value = 1000

for i in range(number_of_elements):
    numbers.append(random.randint(0, max_value))
print(numbers)
start = time.time_ns()
numbers.sort()
end = time.time_ns()
print(numbers)
print("Time taken: ", (end - start)/1000000000)
