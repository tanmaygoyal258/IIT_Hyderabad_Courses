import numpy as np
# import the function from your submission "Serial_7.py"
from Serial_8 import mutual_information
# generating a probability mass function ‘pmf’
pmf = np.array([1 for i in range(10000)])
# normalizing the pmf
pmf = pmf / sum(pmf)
# computing the mutual information between
# two random variables X_i and X_j, i not equal to j
# i, j belong to the set {0,1,2,3}
i = 1
j = 1
MI = mutual_information(pmf,i,j)
print(MI)