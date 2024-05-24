import os,binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from aesLongKeyGen24 import *

#Generate random 3-byte key and expand it
shortKeyBytes = os.urandom(3)
shortKey=bytearray(shortKeyBytes)
print(shortKey.hex())
#Expand key to 128 bits
key=expandKey(shortKey)
print("$",shortKey.hex())
with open("aesShortKey.txt","w") as writer:
    writer.write(shortKeyBytes.hex())
with open("aesLongKey.txt","w") as writer:
    writer.write(key.hex())

#Read from file
#with open("aesLongKey.txt","r") as reader:
#    key_hex=reader.read()
#    key=bytes.fromhex(key_hex)
#Set up iv and cipher
iv=b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
decryptor = cipher.decryptor()

#Read and encrypt messages
ciphertexts=[]
with open("aesPlaintexts.txt","r") as reader:
    messages=reader.read().split('\n')
    for message in messages:
        message_bytes=message.encode('UTF-8')
        #print(message_bytes)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message_bytes) + encryptor.finalize()        
        ciphertexts.append(ciphertext.hex())    

print("Key=",key.hex())
#Add encryption of secret message
with open("aesSecretMessage.txt","r") as read:
    message=read.readline()
    message_bytes=message.encode('UTF-8')
    #print(message_bytes)
    encryptor = cipher.encryptor()
    decryptor=cipher.decryptor()
    secretcipher=encryptor.update(message_bytes)+encryptor.finalize()
    plain=decryptor.update(secretcipher)+decryptor.finalize()
    print("Secret=",secretcipher.hex()," ",plain," ",plain.hex())


#Write to file
with open("aesCiphertexts.txt","w") as writer:
    for ciphertext in ciphertexts:
        writer.write(ciphertext) 
        writer.write("\n")
    writer.write(secretcipher.hex())
