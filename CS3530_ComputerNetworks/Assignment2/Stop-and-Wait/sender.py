import socket
from PIL import Image
import time
# import signal

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
timeout = 0.100
retransmit_num = 0
file_size = 1145 # KB

# Create a UDP socket at reciever side with default timeout value
socket.setdefaulttimeout(timeout)
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Opening Image
img = Image.open('testFile.jpg')
byte_img = img.tobytes()
max_seq = len(byte_img)//1021 + 1

seq_num = 0

start_time = time.time()

while seq_num < max_seq + 1:

    # Creating the required Message
    hex_sequence = hex(seq_num % 2)[2:]
    hex_sequence = hex_sequence.zfill(4)    # 16 bit assuming hexadecimal

    if seq_num == max_seq - 1:
        hex_sequence += '1' # done flag
        msg = byte_img[seq_num * 1021 : ]

    # to close connection
    elif seq_num == max_seq:
        msg = "Request to close Connection"
        try:
            socket_udp.sendto(msg.encode(), recieverAddressPort)
            msgFromServer = socket_udp.recvfrom(bufferSize)

        except socket.timeout:
            print("Retransmitting packet for closing connection")
            retransmit_num += 1
            continue

        else:
            msgString = "Message from Server: {}".format(msgFromServer[0])
            print(msgString)
            print("Closing Connection at Sender's Side")
            break

    else:
        hex_sequence += '0' # done flag
        msg = byte_img[seq_num * 1021 : (seq_num+1) * 1021]

    message = bytearray(len(msg) + 3)
    message[0] = int(hex_sequence[: 2] ,16)         # first byte
    message[1] = int(hex_sequence[2 : 4] , 16)      # second byte
    message[2] = int(hex_sequence[4])             # done flag
    message[3:] = msg

    try:
        # Send to server using created UDP socket
        socket_udp.sendto(message, recieverAddressPort)
        msgFromServer = socket_udp.recvfrom(bufferSize)

    except socket.timeout:
        # no increment in sequence number -> retransmission
        print("Retransmitting packet {}".format(seq_num % 2))
        retransmit_num += 1
        continue

    else:
        # continue onto next sequence number
        msgString = "Message from Server: {}".format(msgFromServer[0])
        print(msgString)
        if msgString[-1] != str(seq_num % 2):
            # acknowledged the wrong packet
            print("Incorrect Acknowledgement, Retransmitting packet {}".format(seq_num % 2))
            retransmit_num += 1
            continue
        else:
            seq_num += 1

end_time = time.time()
print("Time to run {}".format(end_time - start_time))
print("Average Throughput is  {} KB/s".format(file_size / (end_time - start_time)))
print("Number of Retransmissions are {}".format(retransmit_num))
