## This README is dedicated to Assignment 1 of the course CS3530: Computer Networks.

### Author: Tanmay Goyal - AI20BTECH11021

1. Emulating HTTP Server (Basic)
    1. Open a terminal window.
    2. Enter the following commands:<br />
        ```
        cd tutorials/exercises/basic
        make clean
        make run
        ```
    3. On the mininet environment, run `xterm h1 h2` to open two windows for H1 and H2
    4. To capture the pcap traces at H1, make sure line 7 in `client.py` reads
        ```
        input_file = "input1.txt"
        ```
    5. Open another terminal window and type in `sudo wireshark &` and select the `s1-eth1` interface.
    6. In the window for H2, run the following commands: <br />
        ```
        bash h2-arp.sh
        python server.py
        ```
    7. In the window for H1, run the following commands: <br />
         ```
        bash h1-arp.sh
        python client.py
        ```
    8. Stop recording packets in Wireshark and save the captured packets.
    9. To tabulate the timings, ensure that line 7 in `client.py` reads <br />
        ```
        input_file = "input2.txt"
        ```
    10. Open another Wireshaark window by typing in `sudo wireshark &` in the second terminal window and select the `s1-eth1` interface.
    11. Once again, run `python server.py` in the window for H2 and `python client.py` in the window for H1. 
    12. Stop recording packets, and filter by HTTP requests for ease. The timings can now be tabulated.

2. WebCache Development
    1. In the 1st terminal window, move a directory back using:<br />
        ```
        cd ..
        ```
    2. Enter the following commands:<br />
        ```
        cd tutorials/exercises/star
        make clean
        make run
        ```
    3. On the mininet environment, run `xterm h1 h2 h3` to open three windows for H1, H2 and H3.
    4. To capture the pcap traces, make sure line 7 in `client.py` reads <br />
        ```
        input_file = "input1.txt"
        ```
    5. Open another terminal window and type in `sudo wireshark &` and select the `s1-eth1` interface. Similarly, open another two Wireshark windows, and select `s1-eth2` and `s1-eth3` interfaces.
    6. In the window for H3, run the following commands: <br />
         ```
        bash h3-arp.sh
        python server.py
        ```
    7. In the window for H2, run the following commands: <br />
         ```
        bash h2-arp.sh
        python cache.py
        ```
    8. In the window for H1, run the following commands: <br />
         ```
        bash h1-arp.sh
        python client.py
        ```
    9. Stop recording packets in all three windows of Wireshark and save the captured packets.
    10. To tabulate the timings, ensure that line 7 in `client.py` reads <br />
        ```
        input_file = "input2.txt"
        ```
    11. Open another Wireshark window by typing in `sudo wireshark &` in the second terminal window and select the `s1-eth1` interface.
    12. Once again, run `python server.py` in the window for H3, `python cache.py` in the window for H2 and `python client.py` in the window for H1. 
    13. Stop recording packets, and filter by HTTP requests for ease. The timings can now be tabulated.