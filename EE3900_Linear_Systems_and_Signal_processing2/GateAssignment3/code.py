import numpy as np
import matplotlib.pyplot as plt

def u(x):
    res = []
    for i in range(len(x)):
        if x[i] >=0 :
            res.append(1)
        else:
            res.append(0)
    return np.array(res)

N = np.arange(-10,10,1)

plt.stem(N , (0.5**N)*u(N) , 'ko' , label = "$x[n] = (0.5)^n u[n]$")
plt.grid(True)
plt.title("$x[n]$")
plt.legend()
plt.show()

plt.stem(N , (0.25**N)*(u(N)**2) , 'ko' , label = "$y[n] = (0.25)^n u^2[n]$")
plt.grid(True)
plt.title("$y[n]$")
plt.legend()
plt.show()

fourier =  np.fft.fft((0.25**N)*(u(N)**2))
freq=np.fft.fftfreq(fourier.shape[0], d=1/1e5)

plt.plot(freq, np.abs(fourier) ,'-', label = "Fourier transform $Y(e^{j\omega})$")
plt.plot(0 , 4/3 , 'ro' , label = "$Y(e^{j0}) = \\frac{4}{3}$")
plt.grid(True)
plt.title("$Y(e^{j\omega}) =$ Fourier Transform of $y[n]$")
plt.legend(loc = 'lower left')
plt.show()
