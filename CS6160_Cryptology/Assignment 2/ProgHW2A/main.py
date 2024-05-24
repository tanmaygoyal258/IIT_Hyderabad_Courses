from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from aesLongKeyGen24 import *

# defining a class for carrying out a Brute-Force Attack
class BruteForceAttack():

    # defining the constructor
    def __init__(self , message_file , ciphertext_file , IV):

        # reading the ciphertexts and plaintexts
        self.all_ciphers = None
        self.all_messages = None
        with open(message_file , "r") as f:
            self.all_messages = f.readlines()
        with open(ciphertext_file , "r") as f:
            self.all_ciphers = f.readlines()
        self.ciphertexts = [i.split('\n')[0] for i in self.all_ciphers[:-1]]
        self.messages = [i.split('\n')[0] for i in self.all_messages]

        # the last ciphertext is a secret message encoded
        self.secret_ciphertext = self.all_ciphers[-1]
        
        # defining the keys and IV
        self.shortkey = None
        self.key = None
        self.iv = IV

    def attack(self):
        '''
        function to carry out the brute force attack
        '''
        print("Starting Brute Force Attack...")

        for i in range(256):
            for j in range(256):
                # we only need first 4 bits, since the last 4 bits are discarded
                for k in range(16):     
                    
                    # setting the last 4 bits of the last byte zero, similar to shifting right by 4 bits
                    shortkey = [i , j , 16*k]   
                    key = expandKey(shortkey)
                    
                    # defining the cipher and its corresponding decryptor
                    cipher = Cipher(algorithms.AES(key), modes.CBC(self.iv))
                    decryptor = cipher.decryptor()

                    # finding the key
                    all_match = True
                    for m , c in zip(self.messages , self.ciphertexts):
                        m_encoded = m.encode('UTF-8')
                        c_given = cipher.encryptor().update(m_encoded) + cipher.encryptor().finalize()
                        if c != c_given.hex():
                            all_match = False
                            break

                    # if all the ciphertexts match, we have found the key   
                    if all_match:
                        self.key = key
                        self.shortkey = shortkey
                        print("The bytes in the key are: ", shortkey)
                        print("The 20-bit key is: ", bytearray(shortkey).hex())
                        print("The long key is: ", key)                         
                        return
    
    def find_secret_message(self):
        '''
        function to decrypt the secret ciphertext to find the corresponding plaintext
        '''
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        decryptor = cipher.decryptor()
        secret_message = decryptor.update(bytearray.fromhex(self.secret_ciphertext)) + decryptor.finalize()
        print("The secret message is ", secret_message.decode('UTF-8'))


''' ------------------- MAIN ---------------------'''

message_file = '/Users/tanmaygoyal/Desktop/Assignments and Events/Cryptology/Assignment 2/ProgHW2A/aesPlaintexts.txt'
ciphertext_file = '/Users/tanmaygoyal/Desktop/Assignments and Events/Cryptology/Assignment 2/ProgHW2A/aesCiphertexts.txt'

attack = BruteForceAttack(message_file , ciphertext_file , b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
attack.attack()
attack.find_secret_message()