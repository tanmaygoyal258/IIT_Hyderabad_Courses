import numpy as np
import matplotlib.pyplot as plt


T = 0.00004

def x1(t):
    return np.sin(t)

def x2(t):
    return t

# Let T = 1
def y1 (t): 
    return np.cos(t-1) - np.cos(t)
    
def y2(t):
    return 0.5 * (t**2 - (t-1)**2)
    

def y1plusy2(t):
    return np.cos(t-1) - np.cos(t) + 0.5 * (t**2 - (t-1)**2)

def h(t):
    res = []
    for i in range(len(t)):
        if t[i]<T:
            res.append(1)
        else:
            res.append(0)
    return np.array(res)


# plotting fourier transform of impulse response and example input and output signal
t = np.arange(0.0, 0.001, 0.000001)
impulse_fourier =  np.fft.fft(h(t))

f_0 = 10000

x = np.cos(2*np.pi*f_0*t)
y = (np.sin(2*np.pi*f_0*t) - np.sin(2*np.pi*f_0*(t-T)))/(2 * np.pi * f_0)
fourier_input = np.fft.fft(x)
fourier_output = np.fft.fft(y)
freq=np.fft.fftfreq(fourier_input.shape[0], d=1/1e5)

plt.plot(freq, np.abs(impulse_fourier) ,'-', label = "Fourier transform of Impulse response")
plt.plot(freq , np.abs(fourier_input) , label = "Fourier Transform of $x(t) = cos 2 \\pi f_0 t$")
plt.plot(freq , np.abs(fourier_output) , label = "Fourier Transform of $y(t) = \\int_{t-T}^t x(t)\\,dt$")
plt.plot(np.array([1000 for i in range(10)]) , np.array([50*i for i in range(10)]) , 'r--')
plt.plot(np.array([-1000 for i in range(10)]) , np.array([50*i for i in range (10)]) , 'r--')
plt.ylim(0,400)
plt.xlim(-5000,5000)
plt.legend(loc = 'upper right')
plt.grid(True)
plt.show()

# zoomed fourier transforms
plt.plot(freq, np.abs(impulse_fourier) ,'-', label = "Fourier transform of Impulse response")
plt.plot(freq , np.abs(fourier_input) , label = "Fourier Transform of $x(t) = cos 2 \\pi f_0 t$")
plt.plot(freq , np.abs(fourier_output) , label = "Fourier Transform of $y(t) = \\int_{t-T}^t x(t)\\,dt$")
plt.plot(np.array([1000 for i in range(10)]) , np.array([50*i for i in range(10)]) , 'r--')
plt.plot(np.array([-1000 for i in range(10)]) , np.array([50*i for i in range (10)]) , 'r--')
plt.ylim(0,0.5)
plt.xlim(-2000,2000)
plt.legend(loc = 'upper right')
plt.grid(True)
plt.show()

# Plotting input signals
t = np.linspace(-10 , 10, 1000)
plt.plot(t, x1(t) , 'r', label = "$x_1(t) = sin(t)$")
plt.plot(t , x2(t) , 'b', label = "$x_2(t) = t$")
plt.grid(True)
plt.legend(loc = 'upper right')
plt.title("Input signals")
plt.show()

# Plotting output signals
plt.plot(t , y1(t) , 'r', label = "$y_1(t)$")
plt.plot(t , y2(t) , 'b' , label = "$y_2(t)$")
plt.legend(loc = 'upper right')
plt.grid(True)
plt.title("Output Signals: $T = 1$")
plt.show()

# Law of Additivity
plt.plot(t , y1(t) + y2(t) , 'r' , label = "$y_1(t) + y_2(t)$")
plt.plot(t , y1plusy2(t) , 'k--' , label = "System acting on $x_1(t) + x_2(t)$")
plt.legend(loc = 'upper right')
plt.grid(True)
plt.title("Law of Additivity")
plt.show()

# Law of Homogeneity
plt.plot(t , 2 * y1(t)  , 'r' , label = "$2y_1(t)$")
plt.plot(t , 2*(np.cos(t-1) - np.cos(t)) , 'k--' , label = "System acting on $2x_1(t)$")
plt.legend(loc = 'upper right')
plt.grid(True)
plt.title("Law of Homogeneity: $k = 2$")
plt.show()

# Time Invariance
# let us introduce a delay of t_0 = 2
plt.plot(t ,  y1(t-2)  , 'r' , label = "$y_1(t-t_0)$")
plt.plot(t , (np.cos(t-3) - np.cos(t-2)) , 'k--' , label = "System acting on $x_1(t-t_0)$")
plt.legend(loc = 'upper right')
plt.grid(True)
plt.title("Time Invariance")
plt.show()
