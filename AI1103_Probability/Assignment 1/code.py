import numpy as np
from scipy.stats import bernoulli

size = 100000

pr_E = 0.6 #given
pr_F = 0.3 #given
pr_EF = 0.2 #given

data_E = bernoulli.rvs(size = size , p = pr_E)
data_F = bernoulli.rvs(size = size , p = pr_F)

#to find intersection of E and F and find probabilities of E and F
count_EF =0
count_E = 0
count_F = 0


for i in range(size):
  if data_E[i] ==1 and data_F[i]==1:
    count_EF+=1
  if data_E[i] == 1:
    count_E+=1
  if data_F[i] == 1:
    count_F+=1


calc_prob_EF = count_EF/size
calc_prob_E = count_E/size
calc_prob_F = count_F/size

print(calc_prob_EF)


#since Pr(E|F) = Pr(EF)/Pr(F)

print("The calculated value of Pr(E|F) is " , calc_prob_EF/calc_prob_F , "while theoretical value is" , pr_EF/pr_F )

print("The calculated value of Pr(F|E) is " , calc_prob_EF/calc_prob_E , "while theoretical value is" , pr_EF/pr_E )
    


