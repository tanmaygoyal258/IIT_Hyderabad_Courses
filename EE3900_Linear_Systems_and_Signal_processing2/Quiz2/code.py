import numpy as np
import matplotlib.pyplot as plt

N = np.arange(-10,11,1)

def a(N):
    res = []
    for n in N:
        if n%4==0:
            res.append(1)
        else:
            res.append(0)
    return res


plt.stem(N, a(N), 'ro')
plt.title("$a(n)$")
plt.grid(True)
#plt.ylim(0,4)
plt.show()

plt.plot(0,0,'rx', lw = 3 )
plt.plot(10,0 , 'rx', lw = 3 )
plt.plot(-10,0 , 'rx', lw = 3 )
plt.grid(True)
plt.axes().set_facecolor(color = "#b3e6ff")
plt.axes().annotate("$z = 0$" , (0,0))
plt.axes().annotate("$z = \\infty$" , (9,0))
plt.axes().annotate("$z = -\\infty$" , (-10,0))
plt.title("ROC")
plt.xlim(-10.01 , 10.01)
plt.xticks([0])
plt.yticks([0])
plt.show()
