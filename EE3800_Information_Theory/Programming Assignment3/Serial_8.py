import numpy as np


def HammingDecoder(y):

    H = np.zeros((4 , 15))

    y_copy = y.copy()

    # calcualting the parity check matrix
    for i in range(4):
        for j in range(15):
            H[i][j] = (j+1) // (2**(3-i)) 
            H[i][j] %= 2

    # calculating the syndrome
    s = (H @ y_copy) % 2

    # if syndrome is all zeros, no difference in encoding and decoding
    if s.sum() == 0:
        return y_copy
    
    # finding the differing position 
    differing_position = (8 * s[0] + 4 * s[1] + 2 * s[2] + s[3]).astype(int)

    # flipping the bit at the differing position
    y_copy[differing_position - 1] = (y_copy[differing_position - 1] + 1) % 2

    return y_copy