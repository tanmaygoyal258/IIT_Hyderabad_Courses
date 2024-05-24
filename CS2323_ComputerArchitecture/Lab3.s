.data
.dword 15
.text 
lui x3 , 0x10000
addi x4 , x3 , 0x0010    # destination memory

ld a0 , 0(x3) # n

factorial:
    addi sp , sp , -16    # creating space for our function
    sd x1 , 8(sp)         # storing return address
    sd a0 , 0(sp)         # storing n
    addi t0 , x0 , 2      # loading t0 with 2
    blt a0 , t0 , one     # if n < 2 since 1! = 0! = 1, jump to one    
    addi a0 , a0 , -1     # n-1
    jal factorial         # calling factorial (n-1)
    ld a0 , 0(sp)         # loading original n    
    ld x1 , 8(sp)         # loading original return address
    add t0 , x0 , a1      # storing fact(n-1) in t0
    beq x0 , x0 , mult    # fact(n) = n * fact(n-1)

cleanup:    
    sd a1 , 0(x4)         # storing factorial at required destination
    addi sp , sp ,16      # popping the stack for that particular factorial
    beq x1 , x0 , exit    # in case return address is to zero, we will exit the recursion
    jalr x0 , x1 , 0      # returning to the next factorial computation

one:
    addi a1 , x0 , 1      # returns 1
    addi sp , sp , 16     # pop stack since we donot require fact(1) anymore
    jalr x0 , x1 , 0      # return to fact(2) computation

mult:
    addi a0 , a0, -1      # reducing a0 , a0 , -1
    beq a0 , x0 , cleanup
    add a1 , a1 , t0      # doing repeated addition
    beq x0 , x0 , mult
     
exit:
    beq x0 , x0 , exit