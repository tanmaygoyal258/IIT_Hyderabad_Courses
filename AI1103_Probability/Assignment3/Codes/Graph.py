import numpy as np
import matplotlib.pyplot as plt


def f(x):
  if (x>=-1) and (x<=1):
    return 0.2
  elif (x<=-1) and (x>=-4):
    return 0.1
  elif (x>=1) and (x<=4):
    return 0.1
  else:
     return 0

X = np.linspace(-5,5,1000000)

Y = [f(x) for x in X]

plt.plot(X,Y)
plt.xlabel('$x_i$')
plt.ylabel('$f(x_i)$')

plt.show()
