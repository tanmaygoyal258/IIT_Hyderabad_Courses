from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from aesLongKeyGen16 import *

# defining a class for carrying out a Brute-Force Attack
class Meet_Middle_Attack():

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
        self.shortkey1 = None
        self.key1 = None
        self.shortkey2 = None
        self.key2 = None
        self.iv = IV

    def attack(self):
        '''
        function to carry out the Meet-in-the-Middle attack
        '''
        print("Starting Meet-in-the-Middle Attack...")

        # we create the tables for the first m and c
        m = self.messages[0]
        c = self.ciphertexts[0]

        # we store Enc(m,k1)
        encryption_table = {}
        
        # populating the encryption table
        for key1_1 in range(256):
            for key1_2 in range(256):
                    shortkey1 = bytearray([key1_1 , key1_2])
                    key1 = expandKey(shortkey1)
                    
                    # defining the cipher and storing the encryption under the key
                    cipher = Cipher(algorithms.AES(key1), modes.CBC(self.iv))
                    m_encoded = m.encode('UTF-8')
                    encryption_table[(cipher.encryptor().update(m_encoded) + cipher.encryptor().finalize()).hex()] = (key1_1 , key1_2)
        

        # For each possible key2, we check if there is a correponding key1 which gave us the same middle message
        possible_candidates = []

        for key2_1 in range(256):
            for key2_2 in range(256):
                    shortkey2 = bytearray([key2_1 , key2_2])
                    key2 = expandKey(shortkey2)
                    
                    # defining the cipher and storing the decryption under the key
                    cipher = Cipher(algorithms.AES(key2), modes.CBC(self.iv))
                    decryptor = cipher.decryptor()
                        
                    # checking if Dec(c,k2) lies in the encryption table, it is a possible candidate
                    if (decryptor.update(bytearray.fromhex(c)) + decryptor.finalize()).hex() in encryption_table.keys():
                        corresponding_key1 = encryption_table[(decryptor.update(bytearray.fromhex(c)) + decryptor.finalize()).hex()]
                        possible_candidates.append((corresponding_key1 , (key2_1 , key2_2)))

        if len(possible_candidates) == 0:
            print("No possible candidates found")
        
        else:
            # we check for all possible candidates if they are valid
            for keys in possible_candidates:
                
                shortkey1 = [keys[0][0] , keys[0][1]]
                shortkey2 = [keys[1][0] , keys[1][1]]
                key1 = expandKey(shortkey1)
                key2 = expandKey(shortkey2)
                
                cipher1 = Cipher(algorithms.AES(key1), modes.CBC(self.iv))
                cipher2 = Cipher(algorithms.AES(key2), modes.CBC(self.iv))

                all_match = True
                for m,c in zip(self.messages , self.ciphertexts):
                    m_encoded = m.encode('UTF-8')
                    c1 = cipher1.encryptor().update(m_encoded) + cipher1.encryptor().finalize()
                    c2 = cipher2.encryptor().update(c1) + cipher2.encryptor().finalize()
                    if c2.hex() != c:
                        all_match = False
                        break

                if all_match:
                    self.shortkey1 = shortkey1
                    self.key1 = key1
                    self.shortkey2 = shortkey2
                    self.key2 = key2
                    print("The first shortkey is ", bytearray(self.shortkey1).hex())
                    print("The second shortkey is ", bytearray(self.shortkey2).hex())
        return

    def find_secret_message(self):
        '''
        function to decrypt the secret ciphertext to find the corresponding plaintext
        '''
        cipher1 = Cipher(algorithms.AES(self.key1), modes.CBC(self.iv))
        cipher2 = Cipher(algorithms.AES(self.key2), modes.CBC(self.iv))
        decryptor1 = cipher1.decryptor()
        decryptor2 = cipher2.decryptor()

        decrypted = decryptor2.update(bytearray.fromhex(self.secret_ciphertext)) + decryptor2.finalize()
        secret_message = decryptor1.update(decrypted) + decryptor1.finalize()

        print("The secret message is ", secret_message.decode('UTF-8'))
        return


''' ------------------- MAIN ---------------------'''

message_file = '/Users/tanmaygoyal/Desktop/Assignments and Events/Cryptology/Assignment 2/ProgHW2B/2aesPlaintexts.txt'
ciphertext_file = '/Users/tanmaygoyal/Desktop/Assignments and Events/Cryptology/Assignment 2/ProgHW2B/2aesCiphertexts.txt'

attack = Meet_Middle_Attack(message_file , ciphertext_file , b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')
attack.attack()
attack.find_secret_message()