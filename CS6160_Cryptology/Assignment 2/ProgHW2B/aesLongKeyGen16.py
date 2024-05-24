#Expands a 2-byte input into 16 bytes
def expandKey(shortKey):    
    shortKeyval1=shortKey[0]
    shortKeyval2=shortKey[1]    
    
    ByteA=shortKeyval1.to_bytes(1,"big")
    ByteB=shortKeyval2.to_bytes(1,"big")
    ByteC=(shortKeyval1^shortKeyval2).to_bytes(1,"big")
    hexByte1=0x94
    Byte1=hexByte1.to_bytes(1,"big")
    hexByte2=0x5a
    Byte2=hexByte2.to_bytes(1,"big")
    hexByte3=0xe7
    Byte3=hexByte3.to_bytes(1,"big")
    
    longKey=bytearray(ByteA)    
    longKey.extend(Byte1)
    longKey.extend(ByteB)    
    longKey.extend(Byte2)
    
    for i in range(4,9):        
        hexByte=(longKey[i-1]+longKey[i-4])%257
        if (hexByte==256):
            hexByte=0
        Byte=hexByte.to_bytes(1,"big")              
        longKey.extend(Byte)
    longKey.extend(ByteC)
    longKey.extend(Byte3)
    for i in range(11,16):
        hexByte=(longKey[i-1]+longKey[i-4])%257
        if (hexByte==256):
            hexByte=0
        Byte=hexByte.to_bytes(1,"big")              
        longKey.extend(Byte)    
    
    return longKey

#Test key expansion
'''shortKey=bytearray([0xa1,0xb2,0xc3])
longKey1=expandKey(shortKey)
print(longKey1)'''