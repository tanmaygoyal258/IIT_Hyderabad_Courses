
import numpy as np
import matplotlib.pyplot as plt


x = np.linspace(-5,5,1000)

z =  (7 - 9*x)/6
a = (-6 - 3*x)/2


plt.plot(x ,z , 'b-' , label = "$(9,6) \\vec{x} - 7 = 0$")
plt.plot(x , a , 'r-' , label = "$(3,2)\\vec{x} + 6 = 0$")
plt.plot(x , (z + a)/2 , 'k-' , label = "Equidistant line : $(3,2)\\vec{x} - \\frac{11}{6} = 0$")
plt.grid(True)
plt.legend()
plt.title("Equidistant line from a set of Parallel lines")
plt.show()
