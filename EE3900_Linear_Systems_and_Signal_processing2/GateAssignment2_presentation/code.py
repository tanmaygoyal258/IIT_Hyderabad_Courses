import numpy as np
import matplotlib.pyplot as plt

def u(x):
    res = []
    for i in range(len(x)):
        if x[i] >=0 :
            res.append(1)
        else:
            res.append(0)
    return res



n, radii = 50, [0.25 , 0.5]
pole1 = [0.25,0]
pole2 = [0.5 , 0]
zero = [3/8,0]

theta = np.linspace(0, 2*np.pi, n, endpoint=True)
xs = np.outer(radii, np.cos(theta))
ys = np.outer(radii, np.sin(theta))

# in order to have a closed area, the circles
# should be traversed in opposite directions
xs[1,:] = xs[1,::-1]
ys[1,:] = ys[1,::-1]

n, radii = 50, [0.5,1]
theta = np.linspace(0, 2*np.pi, n, endpoint=True)
xs1 = np.outer(radii, np.cos(theta))
ys1 = np.outer(radii, np.sin(theta))

# in order to have a closed area, the circles
# should be traversed in opposite directions
xs1[1,:] = xs1[1,::-1]
ys1[1,:] = ys1[1,::-1]
ax = plt.subplot(111, aspect='equal')
ax.fill(np.ravel(xs), np.ravel(ys), edgecolor='#348ABD' , label = "$\\frac{1}{4}< |z| < \\frac{1}{2}$")
ax.fill(np.ravel(xs1), np.ravel(ys1), edgecolor='#000000' , label = "$\\frac{1}{2} < |z| < 1$")
plt.plot(np.sin(theta), np.cos(theta) , 'k-' , label = "Unit Circle: $|z| = 1$")
plt.plot([pole1[0] , pole2[0]] , [pole1[1],pole2[1]] , 'rx' , label = "Poles of $H(z)$")
plt.plot(zero[0] , zero[1] , 'ro' , label = "Zeroes of $H(z)$")
plt.title("Pole-Zero Plot with ROC")
plt.grid(True)
plt.legend()
plt.show()

X = np.arange(-10 , 10 , 1)

plt.stem(X , (0.5**X + 0.25**X)*u(X) , 'ko' , label = "$h[n] = \\frac{1}{2}^n u[n] + \\frac{1}{4}^n u[n]$")
plt.grid(True)
plt.title("When ROC = $|z| > \\frac{1}{2}$")
plt.legend()
plt.show()

plt.stem(X , (0.25**X)*u(X) - (0.5**X)*u(-X-1) , 'ko' , label = "$h[n] = \\frac{1}{4}^n u[n] - \\frac{1}{2}^n u[-n-1]$")
plt.grid(True)
plt.title("When ROC = $\\frac{1}{4} < |z| < \\frac{1}{2}$")
plt.legend()
plt.show()


X = np.arange(-5,5,1)
plt.stem(X , -(0.25**X)*u(-X-1) - (0.5**X)*u(-X-1) , 'ko' , label = "$h[n] = -\\frac{1}{4}^n u[-n-1] - \\frac{1}{2}^n u[-n-1]$")
plt.grid(True)
plt.title("When ROC = $|z| < \\frac{1}{4}$")
plt.legend()
plt.show()
