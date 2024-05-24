import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-5,5,1000)

def g(x):
    res = []
    for i in x:
        if i>=-1 and i<0:
            res.append(-i)
        else:
            res.append(0)
    return res

plt.plot(t , g(t) , 'k-' , label = '$g(t)$')
plt.grid(True)
plt.title("$g(t)$")
plt.legend()
plt.show()


fourier =  np.fft.fft(g(t))
freq=np.fft.fftfreq(fourier.shape[0], d=1/1e5)
plt.subplot(1,2,1)
plt.plot(freq, np.abs(fourier) ,'k-')
plt.grid(True)
plt.title("$|G(f)|$")
plt.subplot(1,2,2)
plt.plot(freq , np.angle(fourier)  , 'k-')
plt.grid(True)
plt.title("$\\angle(G(f))$")
plt.suptitle("$G(f)$")
plt.show()

plt.plot(t, g(-t) , 'k-' , label = "$g_1(t)$")
plt.grid(True)
plt.title("$g_1(t)$")
plt.legend()
plt.show()


fourier_1 =  np.fft.fft(g(-t))
freq=np.fft.fftfreq(fourier_1.shape[0], d=1/1e5)
plt.subplot(1,2,1)
plt.plot(freq, np.abs(fourier_1) ,'k-')
plt.grid(True)
plt.title("$|G_1(f)|$")
plt.subplot(1,2,2)
plt.plot(freq , np.angle(fourier_1)  , 'k-')
plt.grid(True)
plt.title("$\\angle(G_1(f))$")
plt.suptitle("$G_1(f)$")
plt.show()

plt.plot(t , g(-t - 1) , 'k-' , label = "$g_2(t)$")
plt.grid(True)
plt.title("$g_2(t)$")
plt.legend()
plt.show()

fourier_2 =  np.fft.fft(g(-t-1))
freq=np.fft.fftfreq(fourier_2.shape[0], d=1/1e5)
plt.subplot(1,2,1)
plt.plot(freq, np.abs(fourier_2) ,'k-')
plt.grid(True)
plt.title("$|G_2(f)|$")
plt.subplot(1,2,2)
plt.plot(freq , np.angle(fourier_2 ) , 'k-')
plt.grid(True)
plt.title("$\\angle(G_2(f))$")
plt.suptitle("$G_2(f)$")
plt.show()

plt.plot(t , np.array(g(-t-0.5)) + np.array(g(t-0.5)) , 'k-' , label = "$g_3(t)$")
plt.grid(True)
plt.title("$g_3(t)$")
plt.legend()
plt.show()

plt.figure(figsize = [10, 5])
fourier_3 =  np.fft.fft(np.array(g(-t-0.5)) + np.array(g(t-0.5)))
freq=np.fft.fftfreq(fourier_3.shape[0], d=1/1e5)
plt.subplot(1,2,1)
plt.plot(freq, np.abs(fourier_3) ,'k-')
plt.grid(True)
plt.xlim(-10000,10000)
plt.title("$|G_3(f)|$")
plt.subplot(1,2,2)
plt.plot(freq , np.angle(fourier_3)  , 'k-')
plt.grid(True)
plt.xlim(-10000,10000)
plt.title("$\\angle(G_3(f))$")
plt.suptitle("$G_3(f)$")
plt.show()
