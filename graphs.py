from matplotlib import pyplot as plt
import numpy as np
import math
import time
from matplotlib import style
style.use('ggplot')
x = []
y = []
max_val = 2*3.141592635
divisions = 50

for i in range(divisions):
    x.append(max_val*i/divisions)
    y.append(math.sin(max_val*i/divisions))

plt.title("Sin")
plt.ylabel("Sin(x)")
plt.xlabel("x")

plt.scatter(x, y, color="orange",linewidth=2, label='sin(X)')

#plt.legend()
#plt.grid(True, color='k')

plt.show()

