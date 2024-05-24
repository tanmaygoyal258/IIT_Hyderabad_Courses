## This README is dedicated to Assignment-3 for CS5040-Linear Optimization.

### AUTHORS:
1. Ansh Raninga : EE20BTECH11043
2. Tanay Yadav : AI20BTECH11026
3. Tanmay Goyal : AI20BTECH11021
4. Tanmay Shah : EE20BTECH11061

We have to implement the Simplex Algorithm given the following assumptions:
1. Rank of A is $n$


The input is CSV file with $m+2$ rows and $n+1$ columns. 
1. The first row excluding the last element is the initial feasible point $z$ of length $n$
2. The second row excluding the last element is the cost vector $c$ of length $n$
3. The last column excluding the top two elements is the constraint vector $b$ of length $m$
4. Rows third to $m+2$ and column one to $n$ is the matrix A of size $m\times n$

Run the following commands: <br /> 
```
cd Assignment3
python3 Assignment3.py
```
