import random
import numpy as np

#let the set X be [x1, x2]
#let the set Y be represented by its indices [1 2 3 4 5 6 7...20]

Y = np.linspace(1,20,20).astype(int)
print("The set Y is: ", Y)
# we would select 2 random elements which would map to x1 and x2

sample_size = 100000
count = 0
for i in range(sample_size):
  y1 = random.randint(1,20)
  y2 = random.randint(1,20)
  if(y1!=y2):
    count+=1 # counting for one to one functions

print("The simulated probability is: ", count/sample_size)
print("The theoretical probability is: 0.95")