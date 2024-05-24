import random
import numpy as np

size = 100000
mu = 2
sigma = 2 * (2**0.5) #obtained by R(0)

data_normal = np.random.normal(mu,sigma,size)

count = 0
for i in range(size):
  if (data_normal[i]<=1):
    count+=1

print("The simulated probability is: ", count/size)
print("The theoretical probability is Q(0.3535) = 0.361857")
