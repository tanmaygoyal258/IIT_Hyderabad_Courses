
.data
#The following line defines the 10 values present in the memory.
# We would use different values in our evaluation and
# hence you should try various combinations of these values in your testing.
.dword 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009
#(dword stands for doubleword)    

.text
    #The following line initializes register x3 with 0x10000000 
    #so that you can use x3 for referencing various memory locations. 
    lui x3, 0x10000
    #your code starts here    
    
    
   #    WRITE YOUR CODE HERE
 
    
    #The final result (sum) should be in register x10
    ld x10 ,0(x3) # 1st number stored
    ld x9 , 8(x3) 
    add x10 , x10 , x9 # 2nd number added
    ld x9 , 16(x3)
    add x10 , x10 , x9 # 3rd number added
    ld x9 , 24(x3)
    add x10 , x10 , x9 # 4th number added
    ld x9 , 32(x3)
    add x10 , x10 , x9 # 5th number added
    ld x9 , 40(x3)
    add x10 , x10 , x9 # 6th number added
    ld x9 , 48(x3)
    add x10 , x10 , x9 # 7th number added
    ld x9 , 56(x3)
    add x10 , x10 , x9 # 8th number added
    ld x9 , 64(x3)
    add x10 , x10 , x9 # 9th number added
    ld x9 , 72(x3)
    add x10 , x10 , x9 # 10th number added
    
    
    