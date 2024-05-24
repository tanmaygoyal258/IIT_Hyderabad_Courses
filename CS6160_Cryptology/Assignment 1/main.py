# CRYPTOLOGY PROGRAMMING ASSIGNMENT 1
# SHOWING THE MULTI-TIME PAD IS INSECURE

def convert_hexa_to_decimal(hexa):
    '''
    function to convert hexadecimal string(base 16) to decimal number(base 10)
    '''
    try:
        num1 = int(hexa[0])
    except:
        num1 = 10 + ord(hexa[0]) - ord('a')
    try:
        num2 = int(hexa[1])
    except:
        num2 = 10 + ord(hexa[1]) - ord('a')

    return num1*16 + num2


def ciphertext_to_array(message):
    '''
    function to split the ciphertext, 2 bytes at a time, and store them in an array
    '''
    m = []
    for i in range(0 , len(message) , 2):
        m.append(convert_hexa_to_decimal(message[i:i+2]))
    
    return m


def valid_character(x):
    '''
    function to check if a character is valid or not
    By Validity, we want to check if the character could potentially have been XORed with a space, 
    allowing us to guess
    
    (x >= 65 and x <= 90): if x was a small English alphabet, and was XORed with a space
    (x >= 97 and x <= 122): if x was a capital English alphabet, and was XORed with a space
    (x == 0): if x was a space, XORed with a space
    (x == 12): if x was a comma, XORed with a space
    (x == 26): if x was a period, XORed with a space
    (x == 14): if x was a question mark, XORed with a space
    '''
    return (x >= 65 and x <= 90) or (x >= 97 and x <= 122) or (x == 0) or (x == 12) or (x == 26) or (x == 14)


def ciphertext_pairwise_xor(c1 , c2):
    '''
    function to calculate the pairwise XORs of ciphertexts
    '''
    xor = []
    # we iterate over the minimum length of either of the ciphertexts, rest is unaffected
    for i in range(min(len(c1) , len(c2))):
        xor.append(c1[i] ^ c2[i])

    return xor

def new_entry_dict(dict , key):
    '''
    function to add a new entry to the dictionary
    '''
    if key not in dict.keys():
        dict[key] = 1
    else:
        dict[key] += 1


def decrypt(pairwise_xor , messages):
    '''
    function to find whatever characters we can using the fact that some of them are spaces
    '''
    for i in range(len(pairwise_xor)):
        for j , pairwise_xored in enumerate(pairwise_xor[i]):
            for idx , char in enumerate(pairwise_xored):
                
                # either of the messages, m1 or m2 could contain a not-* character, where * is dummy char
                if messages[i][idx] != '*':
                    messages[i + 1 + j][idx] = chr(ord(messages[i][idx]) ^ char)

                if messages[i + 1 + j][idx] != '*':
                    messages[i][idx] = chr(ord(messages[i + 1 + j][idx]) ^ char)

    return messages

def decrypt_with_key(ciphertext , key):
    '''
    Function to decrypt the ciphertext with the key, however the key may be longer than the text
    or the key may be incomplete, this has to be taken into consideration
    '''

    m = []
    for i in range(len(key)):
        if key[i] == '*' or i >= len(ciphertext):
            break
        else:
            m.append(chr(ciphertext[i] ^ key[i]))

    return m

def array_to_hexa_to_string(arr):
    '''
    function to convert the values in an array to hex, and the concatenate them
    in a string
    '''
    s = ""

    for k in arr:
        num1 = k // 16
        num2 = k % 16
        if num1 >= 10:
            num1 = chr(ord('a') + (num1 - 10))
        if num2 >= 10:
            num2 = chr(ord('a') + (num2 - 10))
        s += str(num1) + str(num2)

    return s
     


''' ------------------- MAIN ---------------------'''

# reading the ciphertexts from the file
lines = []

# REPLACE FILE NAME HERE
file_name = '/Users/tanmaygoyal/Desktop/Assignments and Events/Cryptology/streamciphertexts.txt'    

with open(file_name , 'r') as f:
    for line in f.readlines():
        lines.append(line.strip('\n'))

# converting the ciphertexts to arrays
ciphertexts = []
# ciphertexts = [[45,69] , [108,7] , [47,2] , [39,31]]
for i in lines:
    ciphertexts.append(ciphertext_to_array(i))

# dict of dicts to find the potential spaces in each message
potential_spaces = {}
for i in range(len(ciphertexts)):
    potential_spaces[i] = {}

# making dummy messages which we shall replace as we find out each character
messages = []
for c in ciphertexts:
    messages.append(["*"]*len(c))

# calculating the pairwise XORs of the ciphertexts
pairwise_xor = []
for i in range(len(ciphertexts)):
    xor_i = []
    
    for j in range(i+1 , len(ciphertexts)):
        xor_i.append(ciphertext_pairwise_xor(ciphertexts[i] , ciphertexts[j]))
    
    pairwise_xor.append(xor_i)

# checking for the validity of each pairwise XOR as defined above
for i in range(len(pairwise_xor)):
    for j , pairwise_xored in enumerate(pairwise_xor[i]):
        for idx , char in enumerate(pairwise_xored):
            
            if valid_character(char):               
                new_entry_dict(potential_spaces[i] , idx)
                new_entry_dict(potential_spaces[i + 1 + j] , idx)

# starting to replace the dummy messages with space values
for message_idx in range(len(potential_spaces)):
    for idx in potential_spaces[message_idx]:

        # this means the space is valid for pairwise XOR for all remaining messages
        if potential_spaces[message_idx][idx] == len(ciphertexts)-1:    
            messages[message_idx][idx] = " "

# decrypting the messages with whatever spaces we have found
# Note that we donot need to repeat this process multiple times
m = decrypt(pairwise_xor , messages)

# we print the messages to obtain the following:
    # ***r*pt, then MAC, is the corr*ct*order *or*secure aue**nticated encryption.
    # ***t*is is coffee, please brin* m* some *ea* but if ty** is tea, please brin*********************************
    # *** *robability that we may fa*l *n the *tr*ggle oughe**ot to deter us from *************************************************************
    # *** *ne who consider arithmeti*al*method* o* producinv**andom digits, is of *******************************************
    # ***r* seeing right now that a *as* extin*ti*n can be r**sed by human beings.******************
    # ***a*job interview, tell them *ou*re wil*in* to give  ** perecent. Unless th************************
    # ***e* put off till tomorrow wh*t *ou can*do*the day aw**r tomorrow just as w****
    # ***n*I was a kid, my parents m*ve* a lot* b*t I alwayb**ound them. Rod Dange******
    # *** *ure for boredom is curios*ty* There*s *o cure foc**uriosity. Dorothy Pa****
    # *** *illing time while I wait *or*life t* s*ower me wx** meaning and happine*********************
    # ***a*e memorized this utterly *se*ess pi*ce*of informp**on long enough to pa*************************************
    # ***o*knowledge interactive pro*f:*whatev*r *ou could r**pute before you inte****************************************************************

# From this, we can guess the first message is the following
    # "Encrypt, then MAC, is the correct order for secure authenticated encryption."
# We now hardcode this

sentence1 = "Encrypt, then MAC, is the correct order for secure authenticated encryption."
s1 = []
for c in sentence1:
    s1.append(c)

# finding the key now that we have a valid message
key = ['*'] * 200
for i in range(len(s1)):
    key[i] = ord(s1[i]) ^ ciphertexts[0][i]

# finding all the correct messages with the key we have
correct_messages = []
for i in range(len(ciphertexts)):
    correct_messages.append(decrypt_with_key(ciphertexts[i] , key))

# Once again we print the messages we have to get the following
    # Encrypt, then MAC, is the correct order for secure authenticated encryption.
    # If this is coffee, please bring me some tea; but if this is tea, please brin
    # The probability that we may fail in the struggle ought not to deter us from 
    # Any one who consider arithmetical methods of producing random digits, is of 
    # We're seeing right now that a mass extinction can be caused by human beings.
    # At a job interview, tell them you're willing to give 110 perecent. Unless th
    # Never put off till tomorrow what you can do the day after tomorrow just as w
    # When I was a kid, my parents moved a lot, but I always found them. Rod Dange
    # The cure for boredom is curiosity. There's no cure for curiosity. Dorothy Pa
    # I'm killing time while I wait for life to shower me with meaning and happine
    # I have memorized this utterly useless piece of information long enough to pa
    # Zero-knowledge interactive proof: whatever you could compute before you inte

# From this, we look up the 3rd message to obtain the following
    # "The probability that we may fail in the struggle ought not to deter us from the support of a cause we believe to be just. Abraham Lincoln"
# We hard code this as well

sentence3 = "The probability that we may fail in the struggle ought not to deter us from the support of a cause we believe to be just. Abraham Lincoln"
s3 = []
for c in sentence3:
    s3.append(c)

# finding the key again now that we have a longer correct message
for i in range(len(s3)):
    key[i] = ord(s3[i]) ^ ciphertexts[2][i]

# finding all the correct messages with the key we have
correct_messages = []
for i in range(len(ciphertexts)):
    correct_messages.append(decrypt_with_key(ciphertexts[i] , key))

# We now get the set of correct messages as:
    # Encrypt, then MAC, is the correct order for secure authenticated encryption.
    # If this is coffee, please bring me some tea; but if this is tea, please bring me some coffee. Abraham Lincoln
    # The probability that we may fail in the struggle ought not to deter us from the support of a cause we believe to be just. Abraham Lincoln
    # Any one who consider arithmetical methods of producing random digits, is of course, in a state of sin. John von Neumann
    # We're seeing right now that a mass extinction can be caused by human beings. Elizabeth Kolbert
    # At a job interview, tell them you're willing to give 110 perecent. Unless the job is a statistician.
    # Never put off till tomorrow what you can do the day after tomorrow just as well.
    # When I was a kid, my parents moved a lot, but I always found them. Rod Dangerfield
    # The cure for boredom is curiosity. There's no cure for curiosity. Dorothy Parker
    # I'm killing time while I wait for life to shower me with meaning and happiness. Calvin and Hobbes
    # I have memorized this utterly useless piece of information long enough to pass a test question. Calvin and Hobbes
    # Zero-knowledge interactive proof: whatever you could compute before you interacted with me and afterward are not different. Shafi Goldwas

# Note that the longest sentence, the last one is still incomplete. A small Google Search gives us the following
correct_messages[-1].append('s')
correct_messages[-1].append('e')
correct_messages[-1].append('r')

# Thus, we can now obtain the first and the final message
print("\nThe first message is: ")
print(''.join(correct_messages[0]))
print("\nThe final message is:")
print(''.join(correct_messages[-1])) 

# printing the first 140 bytes of the key
# we donot have any information of the remaining 60 bytes and hence, cannot randomly guess them
for i in range(len(correct_messages[-1])):   # choosing the longest message
    key[i] = ord(correct_messages[-1][i]) ^ ciphertexts[-1][i]

# writing the key to the output file
print("\nThe key has been stored in the file key.txt:\n", array_to_hexa_to_string(key[0:2]))

with open('key.txt' , 'w') as f:
    f.write(array_to_hexa_to_string(key[:140]))