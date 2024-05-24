import numpy as np
import random

size = 100000
count = 0
for i in range(size):
  #between -4 and -1 
  a = random.uniform(-4,-1)
  #between -1 and 0
  b = random.uniform(-1,0)
  #between 0 and 1
  c = random.uniform(0,1)
  #between 1 and 4
  d = random.uniform(1,4)
  #final random variable X
  X = np.random.choice([a,b,c,d] , p=[0.3,0.2,0.2,0.3])
  #Pr(a<=X<= b) = integral f(x)dx with lower limit a and upper limit b
  
  if(X<5) and (X>0.5):
    count+=1

#pr(0.5<X<5) = count/size
#theoretically, we get pr(0.5<X<5) = 0.4
print("The probability that X lies between 0.5 and 5 is ", count/size)
