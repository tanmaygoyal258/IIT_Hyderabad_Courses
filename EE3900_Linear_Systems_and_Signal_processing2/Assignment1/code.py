import matplotlib.pyplot as plt
import numpy as np
A  = np.array([-1, 0])
B = np.array([3, 1])
C = np.array([2, 2])
D = np.array([-2,1])
E = (A + B)/2
F = (B + C)/2
G = (C + D)/2
H = (A + D)/2
P = (E + G)/2

plt.plot([A[0] , B[0]] ,[A[1], B[1]], 'r-')
plt.plot([B[0], C[0]] ,[B[1] , C[1]] , 'k-' )
plt.plot([C[0] , D[0]] , [C[1] , D[1]] , 'r-')
plt.plot([A[0] , D[0]] , [A[1] , D[1]] , 'k-')
plt.plot([E[0] , G[0]] , [E[1] , G[1]] , 'c-')
plt.plot([F[0] , H[0]] , [F[1] , H[1]] , 'c-')
plt.plot(A[0] , A[1] , 'bo')
plt.plot(B[0] , B[1] , 'bo')
plt.plot(C[0] , C[1] , 'bo')
plt.plot(D[0] , D[1] , 'bo')
plt.plot(E[0] , E[1] , 'go')
plt.plot(F[0] , F[1] , 'go')
plt.plot(G[0] , G[1] , 'go')
plt.plot(H[0] , H[1] , 'go')
plt.plot(P[0] , P[1] , 'mo')
plt.text(A[0]+0.1 , A[1]-0.08 , "A(-1,0)" , fontsize = 12 , color = 'b')
plt.text(B[0]+0.1 , B[1], "B(3,1)" , fontsize = 12 , color = 'b')
plt.text(C[0]+0.1 , C[1] , "C(2,2)" , fontsize = 12 , color = 'b')
plt.text(D[0]-0.2 , D[1]+0.1 , "D(-2,1)" , fontsize = 12 , color = 'b')
plt.text(E[0]-0.1 , E[1] - 0.2, "E(1,0.5)" , fontsize = 12 , color = 'g')
plt.text(F[0]+0.1 , F[1] , "F(2.5,1.5)" , fontsize = 12 , color = 'g')
plt.text(G[0]-0.2 , G[1]+0.15 , "G(0,1.5)" , fontsize = 12 , color = 'g')
plt.text(H[0] + 0.2 , H[1] - 0.1 , "H(-1.5,0.5)" , fontsize = 12 , color = 'g')
plt.text(P[0]+0.2 , P[1]-0.1 , "P(0.5,1) = Q(0.5,1)" , fontsize = 10 , color = 'm')
plt.grid(True)
plt.title("Parallelogram")
plt.show()