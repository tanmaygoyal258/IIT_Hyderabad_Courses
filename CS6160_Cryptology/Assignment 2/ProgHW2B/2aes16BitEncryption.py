import os,binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from aesLongKeyGen16 import *

#Subroutine for encryption
def aesEncrypt(message_bytes,cipher):
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message_bytes) + encryptor.finalize()
    return ciphertext
#Subroutine for decryption
def aesDecrypt(message_bytes,cipher):
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(message_bytes) + decryptor.finalize()
    return plaintext

#Generate two random 2-byte keys
shortKeyBytes = os.urandom(2)
shortKey1=bytearray(shortKeyBytes)
shortKeyBytes = os.urandom(2)
shortKey2=bytearray(shortKeyBytes)
with open("2aesShortKeys.txt","w") as writer:
    writer.write(shortKey1.hex())
    writer.write("\n")
    writer.write(shortKey2.hex())    

#Expand keys to 128 bits
longKey1=expandKey(shortKey1)
longKey2=expandKey(shortKey2)
with open("2aesLongKeys.txt","w") as writer:
    writer.write(longKey1.hex())
    writer.write("\n")
    writer.write(longKey2.hex())    

#Read from file
#with open("2aesLongKeys.txt","r") as reader:
#    key_hex=reader.read()
#    key=bytes.fromhex(key_hex)
#Set up iv and ciphers
iv=b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
cipher1 = Cipher(algorithms.AES(longKey1), modes.CBC(iv))
cipher2 = Cipher(algorithms.AES(longKey2), modes.CBC(iv))

#Read and encrypt messages
ciphertexts=[]
with open("2aesPlaintexts.txt","r") as reader:
    messages=reader.read().split('\n')
    for message in messages:
        message_bytes=message.encode('UTF-8')
        #Encrypt with key1
        ciphertext = aesEncrypt(message_bytes,cipher1)        
        #Encrypt again with key2        
        ciphertext2=aesEncrypt(ciphertext,cipher2)       
        ciphertexts.append(ciphertext2.hex())                

#Add encryption of secret message
with open("2aesSecretMessage.txt","r") as read:
    message=read.readline()    
    message_bytes=message.encode('UTF-8')
    #Encrypt
    secretcipher=aesEncrypt(message_bytes,cipher1)
    secretcipher2=aesEncrypt(secretcipher,cipher2)
    #print("Plain=",message_bytes.hex(),"Intermediate=",secretcipher.hex()," Secret=",secretcipher2.hex())
    secretcipher=aesDecrypt(secretcipher2,cipher2)
    plain=aesDecrypt(secretcipher,cipher1)
    #print("Intermediate= ",secretcipher.hex()," Plain=",plain.hex())

#Write to file
with open("2aesCiphertexts.txt","w") as writer:
    for ciphertext in ciphertexts:
        writer.write(ciphertext) 
        writer.write("\n")
    writer.write(secretcipher2.hex())
