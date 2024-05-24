import numpy as np

def entropy(pmf):
    # returns the entropy given a valid pmf
    h = 0
    # we could have directly used numpy instead of a for loop, but that would give error if any element is 0
    for p in pmf:
        if p == 0:
            continue
        else:
            h += p * np.log2(p)
    
    return -h 

def mutual_information(pmf , i , j):
    # calculates the mutual information between two random variables X_i and X_j
    # using the formula I(X_i ; X_j) = H(X_i) + H(X_j) - H(X_i , X_j)
    # since we have 4 random variables, the pmfs can be calculated by summing over the remaining variables
    # we also know, all random variables X_i take values between {0,1,2,3,4,5,6,7,8,9}

    # parameters : pmf - the joint pmdf of X_0 , X_1 , X_2 , X_3
    #              i , j - the indices of the random variables X_i and X_j

    # pmf for X_i
    pmf_Xi = np.zeros(10)

    # pmf for X_j
    pmf_Xj = np.zeros(10)

    # joint pmf for X_i and X_j
    pmf_Xi_Xj = np.zeros((10,10)) 

    # iterating over the entire joint pmf
    for idx , prob in enumerate(pmf):

        # retrieving the values of X_i and X_j form the array indices
        # in case the index in the string does not exist, we will have to set it to zero
        # for example, 2nd index in string "7" is not defined, so we assume the string to be "0007"
        
        try:
            X_i = int(str(idx)[: : -1][i])
        except:
            X_i = 0

        try:
            X_j = int(str(idx)[: : -1][j])
        except:
            X_j = 0

        # updating the pmfs
        pmf_Xi[X_i] += prob
        pmf_Xj[X_j] += prob
        pmf_Xi_Xj[X_i][X_j] += prob

    # we convert pmf_Xi_Xj into a 1D vector since our enropy function will wrkk only with 1D vectors
    pmf_Xi_Xj = pmf_Xi_Xj.reshape(-1,)

    # returning the mutual information
    return entropy(pmf_Xi) + entropy(pmf_Xj) - entropy(pmf_Xi_Xj)