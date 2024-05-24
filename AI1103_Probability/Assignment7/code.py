import numpy as np
import random

n = 3
p = 0.5
size = 1000000


data_binomial = np.random.binomial(n,p,size)
count = 0
for i in range(size):
  if (data_binomial[i]>=1):
    count+=1

print("The simulated probability is: ",count/size, "while the theoretical probability is: ", 7/8 )