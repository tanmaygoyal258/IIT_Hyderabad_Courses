import numpy as np
import matplotlib.pyplot as plt

def F(x):
  if (x>=-4) and (x<=-1):
    return 0.1 * (x+4)
  elif (x>=-1) and (x<=1):
    return 0.5 + 0.2*x
  elif (x>=1) and(x<=4):
    return 0.6 + 0.1*x
  elif (x>=4):
    return 1;
  else:
      return 0


X = np.linspace(-5,5,1000000)

Y = [F(x) for x in X]
plt.xlabel('$x_i$')
plt.ylabel('$F(x_i)$')
plt.plot(X,Y)
plt.grid()
plt.show()
