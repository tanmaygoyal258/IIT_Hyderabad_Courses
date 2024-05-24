.section .data
L1: .word 0             #This location indicates the error of the result. It is 0 if no error else 1.
.word 2, 2         #x and y dimensions of MATRIX-1
.word 1, 2, 3, 4
.word 2 ,2             #x and y dimensions of MATRIX-2
.word 1,2,3,4

.section .text
.global main

main:
    la x3 , L1
    lw x5 , 4(x3)        # dimension1 of matrix1
    lw x6 , 8(x3)        # dimension2 of matrix1
    mul x7 , x5 , x6    # number of elements in matrix1
    add x8, zero, zero
    addi x8 , x8 , 4    # bytes
    mul x7 , x7 , x8    # number of bytes in matrix1
    addi x3 , x3 , 12
    add x3 , x3 , x7
    lw x28 , 0(x3)    # dimension1 of matrix2
    lw x29 , 4(x3)    # dimension2 of matrix2
    mul x30 , x29 , x28 # number of elements in matrix2
    mul x30 , x30 , x8    # number of bytes in matrix2
    bne x28 , x6 , error
    la x3 , L1
    sw x0 , 0(x3)    # no error
    addi x3 , x3 , 12
    add x3 , x3 , x7
    addi x3, x3 , 8
    add x3 , x3 , x30
    sw x5 , 0(x3)    # dimension1 of product matrix
    sw x29 , 4(x3)    # dimension2 of product matrix
    addi x10 , x0 ,  0  # i
    addi x11 , x0 , 0    # j
    addi x12 , x0 , 0    # k
    addi x13 , x0 , 12    # base pointer for matrix1
    add x14 , x0 , x7
    addi x14 , x14 , 20    # base pointer for matrix 2
    add x15 , x15 , x7
    addi x15 , x15 , 28
    add x15 , x15 , x30    # base pointer for product matrix

MatrixMult:
    # M[i][j] = M1[i][k] * M2[k][j]

    Loop1:
        beq x10 , x5 , exit
    Loop2:
        beq x11 , x29 , EndLoop2
    Loop3:
        beq x12 , x6 , store
        add x18 , x0 , x0
        add x18 , x18 , x13
        mul x19 , x10 , x6
        add x19 , x19 , x12
        mul x19 , x19 , x8
        add x18 , x18 , x19
        # calculating offset for element1 -> (i * D1y + k) * bytes
        la x3 , L1
        add x3 , x3 , x18
        lw x22 , 0(x3)    # element1

        add x18  ,x0 , x0
        add x18 , x18 , x14
        mul x19 , x12 , x29
        add x19 , x19 , x11
        mul x19 , x19 , x8
        add x18 , x18 , x19
        # calculating offset for element2 -> (k * D2y + j) * bytes
        la x3 , L1
        add x3 , x3 , x18
        lw x23 , 0(x3)    # element 2

        mul x24 , x23 , x22
        add x25 , x25 , x24
        # sum of multiplication of entries in x25
        addi x12 , x12 , 1    # increment k by 1
        beq x0 , x0 , Loop3

        store:
            addi x22 , x10 , 0
            addi x23 , x11 , 0
            mul x22 , x22 , x29
            add x22 , x22 , x23
            mul x22 , x22 , x8
            # calculating offset for result element -> (i * D3y + j) * bytes
            la x3 , L1
            add x3 , x3 , x15
            add x3 , x3 , x22
            sw x25 , 0(x3)
            addi x11 , x11 , 1    # incrementing j by 1
            add x12 , x0 , x0    # setting k to 0
            add x25 , x0 , x0    # setting result storage to 0
            beq x0 , x0 , Loop2

        EndLoop2:
            addi x10 , x10 , 1    # increment i by 1
            add x11 , x0 , x0    # set j = 0
            add x12 , x0 , x0    # set k = 0
            add x25 , x0 , x0    # setting result storage to 0
            beq x0 , x0 , MatrixMult



exit:
    j exit

Lwhile1:
j Lwhile1

error:
    addi x31 , x31 , 1
    la x3 , L1
    sw x31 , 0(x3)
    beq x0 , x0 , exit


