from Serial_8 import HammingDecoder
import numpy as np

# Sample output of binary symmetric channel
y = np.array([0,1,1,0,1,1,0,1,0,0,1,1,1,1,0])

# decoding the most likely codeword of the Hamming code
x = HammingDecoder(y)

print(x)
