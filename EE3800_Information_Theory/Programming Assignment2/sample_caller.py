from Serial_8 import lrt

T = 3.5

alpha , beta = lrt(T)

print("Type-1 error: {:.3f}".format(alpha))
print("Type-2 error: {}".format( beta))

