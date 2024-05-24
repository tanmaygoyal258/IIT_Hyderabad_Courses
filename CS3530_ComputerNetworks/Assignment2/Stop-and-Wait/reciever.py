import socket
import time
from PIL import Image

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size
duplicates = 0
photo = ""  

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )

last_recived_seq_num = -1

while True:

    #wait to recieve message from the server
    bytesAddressPair = socket_udp.recvfrom(bufferSize)

    #split the recieved tuple into variables
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1]


    if recievedMessage != "Request to close Connection":
        sequence_number = ord(recievedMessage[0]) * 256 + ord(recievedMessage[1])
        done = ord(recievedMessage[2])

        if last_recived_seq_num == sequence_number:
            # duplicate detected
            print("Discarding Duplicate packet {}".format(sequence_number))
            duplicates += 1
            message = str.encode("Duplicate sequence number: " + str(sequence_number))
            socket_udp.sendto(message, senderAddress)

        else:
            print("Recieved sequence number: " + str(sequence_number))
            last_recived_seq_num = sequence_number
            message = str.encode("Recieved sequence number: " + str(sequence_number))
            socket_udp.sendto(message, senderAddress)
            photo += recievedMessage[3:]

    else: # closing connection
        print(recievedMessage)
        message = str.encode("Closing Connection at Reciever's side")
        socket_udp.sendto(message, senderAddress)
        print("Number of Duplicate Packets recieved {}".format(duplicates))
        print("Closing Connection at Reciever's side")
        img = Image.frombytes('RGB', (1920 , 1080), photo)
        img.show()
        break
