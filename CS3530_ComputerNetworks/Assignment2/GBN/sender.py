import socket
from PIL import Image
import time
# import signal

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
timeout = 0.300
timeout_num = 0
window_size = 256
file_size = 1145 # KB
recived_acknowledgements = []

# Create a UDP socket at reciever side with default timeout value
socket.setdefaulttimeout(timeout)
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Opening Image
img = Image.open('testFile.jpg')
byte_img = img.tobytes()

max_seq = len(byte_img)//1021 + 1

start_time = time.time()

window_start = 0
window_end = window_size - 1
highest_ack = -1

while True:

    if window_end == max_seq + 1:
        break

    for j in range(window_start , window_end + 1):

        if j == max_seq + 1:
            break

        # Creating the required Message
        hex_sequence = hex(j)[2:]
        hex_sequence = hex_sequence.zfill(4)    # 16 bit assuming hexadecimal

        if j == max_seq - 1:
            hex_sequence += '1' # done flag
            msg = byte_img[j * 1021 : ]

        else:
            hex_sequence += '0' # done flag
            msg = byte_img[j * 1021 : (j+1) * 1021]

        message = bytearray(len(msg) + 3)
        message[0] = int(hex_sequence[: 2] ,16)         # first byte
        message[1] = int(hex_sequence[2 : 4] , 16)      # second byte
        message[2] = int(hex_sequence[4])             # done flag
        message[3:] = msg
        # Send to server using created UDP socket
        socket_udp.sendto(message, recieverAddressPort)

    while True:

        if window_end == max_seq + 1:
            break

        try:
            msgFromServer = socket_udp.recvfrom(bufferSize)

        except socket.timeout:
            # no increment in window_start -> retransmission
                print("Timeout... Retransmitting packet {}".format(window_start))
                timeout_num += 1
                break

        else:
            # continue onto next sequence number
            msgString = "Message from Server: {}".format(msgFromServer[0])
            print(msgString)
            recived_acknowledgements.append(int(msgString.split(' ')[-1]))

            # we get next in order packet
            if int(msgString.split(' ')[-1]) == highest_ack + 1 :
                window_start += 1
                window_end += 1
                highest_ack += 1
                retransmitting = False

                if window_end == max_seq + 1:
                    break

                # if we revieve correct ACK, we send the next packet
                hex_sequence = hex(window_end)[2:]
                hex_sequence = hex_sequence.zfill(4)    # 16 bit assuming hexadecimal

                if window_end == max_seq - 1:
                    hex_sequence += '1' # done flag
                    msg = byte_img[window_end * 1021 : ]

                else:
                    hex_sequence += '0' # done flag
                    msg = byte_img[window_end * 1021 : (window_end+1) * 1021]

                message = bytearray(len(msg) + 3)
                message[0] = int(hex_sequence[: 2] ,16)         # first byte
                message[1] = int(hex_sequence[2 : 4] , 16)      # second byte
                message[2] = int(hex_sequence[4])             # done flag
                message[3:] = msg
                # Send to server using created UDP socket
                socket_udp.sendto(message, recieverAddressPort)

            # if the packet has not been acknowledged before
            elif int(msgString.split(' ')[-1]) not in recived_acknowledgements:
                print("Retransmitting packet {}...".format(window_start))
                break

# to close connection
while True:
    if window_end == max_seq + 1:
        msg = "Request to close Connection"
        try:
            socket_udp.sendto(msg.encode(), recieverAddressPort)
            msgFromServer = socket_udp.recvfrom(bufferSize)

        except socket.timeout:
            print("Retransmitting packet for closing connection")
            timeout_num += 1

        else:
            msgString = "Message from Server: {}".format(msgFromServer[0])
            print(msgString)
            print("Closing Connection at Sender's Side")
            break

end_time = time.time()
print("Time to run {}".format(end_time - start_time))
print("Average Throughput is  {} KB/s".format(file_size / (end_time - start_time)))
print("Number of Timeouts are {}".format(timeout_num))
