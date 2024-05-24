# # # Include student submission here # # # # #
from Serial_8 import mutual_information
# # # # # # # # # # # # # # # # # # # # # # # #

import numpy as np
from math import log
np.random.seed(8022023)

def generate_pmf():
    pmf = np.zeros(10_000, dtype=float)
    for a in np.arange(10_000):
        b = a
        avec = [0] * 4
        for i in np.arange(4):
            avec[i] = b % 10
            b = b // 10
        cvec = np.random.randint(1,high=6,size=4)
        dist = 1 + abs((avec[0] - avec[1])**cvec[0]) + abs((avec[1] - avec[3])**cvec[1]) + abs((avec[0] - avec[3])**cvec[2]) + abs((avec[2] - avec[3])**cvec[3])
        pmf[a] = 1/dist

    pmf = pmf / sum(pmf)
    print(pmf)
    return pmf


def mutual_information_eval(pmf,indx,indy):
    # H = 0
    # for p in pmf:
    #    H = H - (p * log(p,2))
    #
    # return H + i + j

    # forming joint pmf matrix for two variables
    P = np.zeros((10,10), dtype=float)

    for a in np.arange(10_000):
        b = a
        avec = [0] * 4
        for i in np.arange(4):
            avec[i] = b % 10
            b = b // 10

        P[avec[indx],avec[indy]] = P[avec[indx],avec[indy]] + pmf[a]

    # computing joint entropy
    Pvec = P.reshape(100)
    Hxy = 0.0
    for p in Pvec:
        Hxy = Hxy - (p * log(p, 2))

    # computing individual entropies
    Px = np.sum(P,axis=0)
    Hx = 0.0
    for p in Px:
        Hx = Hx - (p * log(p, 2))

    Py = np.sum(P,axis=1)
    Hy = 0.0
    for p in Py:
        Hy = Hy - (p * log(p, 2))

    return Hx + Hy - Hxy

score = 0
for i in range(4):
    for j in range(i):

        # generate a pmf
        pmf = generate_pmf()

        # find mutual information from the Student's code
        MI = mutual_information(pmf,i,j)

        # compute using the function included here
        MI_eval = mutual_information_eval(pmf,i,j)

        # allow 5% error
        if abs(MI - MI_eval) < 0.05*MI_eval:
            score = score + 1

score = round(score * (10/6),2)
print(score)
