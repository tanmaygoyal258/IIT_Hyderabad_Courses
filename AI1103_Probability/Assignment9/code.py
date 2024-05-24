import random

size  =100000
count = 0
#Let X=0,1,2 denote red and X=3,4,5,6,7,8 denote black
X = [0,1,2,3,4,5,6,7,8]
for i in range(size):
  count_red = 0
  chosen = random.sample(X,5)
  for i in range(4):
    if (chosen[i]<=2):
      count_red+=1
  if (count_red==1) and (chosen[4]<=2):
    count+=1
 
print("The simulated probability is: ",count/size)
print("The theoretical probability is: 0.19")