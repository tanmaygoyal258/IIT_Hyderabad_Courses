from scipy.stats import poisson
import numpy as np
import random

lamda =  random.randint(0,100)
print("Lamda is: ", lamda)
size = 100
data_poisson = np.random.poisson(lamda,size)

sample_size = 100
total_average = 0
#overall average
for i in range(size):
  average_per_item = 0
  # finding the average for every item in the distribution
  for j in range(sample_size):
    if (data_poisson[i]>1):
       n_1 = random.randint(1,data_poisson[i]) 
    elif (data_poisson[i] == 1):
       n_1 = 1
    else : 
      n_1 = 0
    #since the conditional probability of n_1 given n is uniform and equal
    n_2 = data_poisson[i] - n_1
    average_per_item+=n_2
  average_per_item = average_per_item / sample_size

  total_average += average_per_item

total_average = total_average / size

print("Expected value of N2 from simulation is: ", total_average)
print("Theoretical expected value of N2 is: ", (lamda-1)/2)


