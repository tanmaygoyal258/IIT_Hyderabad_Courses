.data
.dword 100

.text
lui x3, 0x10000

# destination
addi x6 , x3 , 0x100    # memory location for square numbers
addi x7 , x3 , 0x010    # memory location for sum of squares   

# 2n-1
addi x2 , x0 , 1

# backup
add x15 , x0 , x0

# n
ld x1 , 0(x3)

L1: 
    add x15 , x15 , x2        
    sd x15 , 0(x6)        # take the memory location from x6 and store x15 in it
    addi x6 , x6 , 8      # increase the memory location by 8
    addi x2 , x2 , 2
    addi x1 , x1 , -1
    add x9 , x9 , x15     # storing total sum in x9
    
    bne x1 , x0 , L1
    
    sd x9 , 0(x7)         # take memory location x7 and store the sum from x9 in it