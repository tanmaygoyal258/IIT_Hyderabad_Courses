import numpy as np

def lrt(T):
    '''
    This function performs Binary Hypothesis testing on the following hypothesis:
    H1: X1, X2 and X3 are iid with distribution P1
    H2: X1, X2 and X3 are iid with distribution P2

    We are also given the set X, over which X1, X2 and X3 take values
    X = {1 , 2 , 3}

    The distributions are as follows:
    p1(1) = 0.5 , p1(2) = 0.35 , p1(3) = 0.15
    p2(1) = 0.2 , p2(2) = 0.3 , p2(3) = 0.5

    It returns the Type-1 error and Type-2 errors for the deterministic Likelyhood Ratio Tests
    for the following Binary Hypothesis Testing problem, given the threshold T

    Parameters:
        T: the threshold for the LRT

    Returns:
        alpha: Type-1 error
        beta: Type-2 error
    '''

    # defining the distributions
    p1 = np.array([0.5, 0.35, 0.15])
    p2 = np.array([0.2, 0.3, 0.5])

    # note that here we are operating in a 3-dimensional space
    # our possible values include X = [(1,1,1) , (1,1,2) , (1,2,3), ...]

    # we define a 3D matrix as follows (the three variables are i.i.d):
    # Joint_p1[i][j][k] = P1(X1 = i+1, X2 = j+1, X3 = k+1)
    # Joint_p2[i][j][k] = P2(X1 = i+1, X2 = j+1, X3 = k+1)

    Joint_p1 = np.zeros((3, 3, 3))
    Joint_p2 = np.zeros((3, 3, 3))

    for i in range(3):
        for j in range(3):
            for k in range(3):
                Joint_p1[i][j][k] = p1[i] * p1[j] * p1[k]
                Joint_p2[i][j][k] = p2[i] * p2[j] * p2[k]

    # likelihood
    L = Joint_p1 / Joint_p2

    # given T, we find the acceptance region as L > T
    acceptance = L > T
    rejection = L <= T

    # we know type1 error = alpha = P1(rejection region) and type2 error = beta = P2(acceptance region)
    alpha = np.sum(Joint_p1[rejection])
    beta = np.sum(Joint_p2[acceptance])

    return alpha , beta