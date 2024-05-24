import socket
from PIL import Image
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Opening Image
img = Image.open('testFile.jpg')
byte_img = img.tobytes()
max_seq = len(byte_img)//1021 + 1


for i in range(max_seq + 1):

    # Creating the required Message
    hex_sequence = hex(i)[2:]
    hex_sequence = hex_sequence.zfill(4)    # 16 bit assuming hexadecimal

    if i == max_seq - 1:
        hex_sequence += '1' # done flag
        msg = byte_img[i * 1021 : ]

    elif i == max_seq:
        msg = "Request to close Connection"
        socket_udp.sendto(msg.encode(), recieverAddressPort)
        msgFromServer = socket_udp.recvfrom(bufferSize)
        msgString = "Message from Server: {}".format(msgFromServer[0])
        print(msgString)
        print("Closing Connection at Sender's Side")
        break

    else:
        hex_sequence += '0' # done flag
        msg = byte_img[i * 1021 : (i+1) * 1021]

    message = bytearray(len(msg) + 3)
    message[0] = int(hex_sequence[: 2] ,16)         # first byte
    message[1] = int(hex_sequence[2 : 4] , 16)      # second byte
    message[2] = int(hex_sequence[4])             # done flag
    message[3:] = msg

    # Send to server using created UDP socket
    socket_udp.sendto(message, recieverAddressPort)

    #wait for reply message from reciever
    msgFromServer = socket_udp.recvfrom(bufferSize)

    msgString = "Message from Server: {}".format(msgFromServer[0])
    print(msgString)

    time.sleep(0.01)
