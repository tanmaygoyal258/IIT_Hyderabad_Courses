## This README is dedicated to Assignment 2 of the course CS3530: Computer Networks.

### Author: Tanmay Goyal - AI20BTECH11021

1. Basic
    1. Open a terminal window and install the Pillow library using `pip install Pillow`.

    2. Enter the Basic folder in the Assignment2 directory using <br />
        ```
        cd Assignment2/Basic
        ```

    3. Once inside the Basic Folder, run the following two commands <br />
        ```
        sudo mn
        xterm h1 h2
        ```

    4. The shell script files for H1 and H2 have already been created, containing commands to vary the bandwidth of the link, the propogation delay and the packet loss percentage. For this problem, we assume a constant bandwidth of 10Mbps, a delay of 5ms and 0% packet loss. To avoid packet loss we have introduced a 10ms sleep in the sender file.
    
    5. Run the bash files, by typing in the following commands in the respective windows: <br />
        ```
        bash h1-setnet.sh
        bash h2-setnet.sh
        ```

    6. In the window for H2, run
        ```
        python reciever.py
        ```

    7. In the window for H1, run
        ```
        python sender.py
        ```
    

2. Stop-and-Wait
    1. Enter the Stop-and-Wait folder in the Assignment2 directory using <br />
        ```
        cd .. 
        cd Stop-and-Wait
        ```

    2. Once inside the Stop-and-Wait Folder, run the following two commands <br />
        ```
        sudo mn
        xterm h1 h2
        ```

    3. The shell script files for H1 and H2 have already been created, containing commands to vary the bandwidth of the link, the propogation delay and the packet loss percentage. For this problem, we assume a constant bandwidth of 10Mbps , 5ms delay and 5% packet loss.  
    
    4. Run the bash files, by typing in the following commands in the respective windows: <br />
        ```
        bash h1-setnet.sh
        bash h2-setnet.sh
        ```
    
    5. In the window for H2, run
        ```
        python reciever.py
        ```

    6. Adjust the appropriate retransmission timeout by changing the value of the variable `timeout` on line 10.Then, in the window for H1, run
        ```
        python sender.py
        ```

    7. The optimal retransmission timeout is found to be equal to RTT ~ 2 * delay value.


3. Go Back N
    1. Enter the GBN folder in the Assignment2 directory using <br />
        ```
        cd .. 
        cd GBN
        ```

    2. Once inside the GBN Folder, run the following two commands <br />
        ```
        sudo mn
        xterm h1 h2
        ```

    3. The shell script files for H1 and H2 have already been created, containing commands to vary the bandwidth of the link, the propogation delay and the packet loss percentage. For this problem, we assume a constant bandwidth of 10Mbps ,and 0.5% packet loss. The delay needs to be adjusted appropriately.  
    
    4. Run the bash files, by typing in the following commands in the respective windows: <br />
        ```
        bash h1-setnet.sh
        bash h2-setnet.sh
        ```
    Note that, these need to be run only when the bash files are modified, and do not need to be run everytime. 

    5. In the window for H2, run
        ```
        python reciever.py
        ```

    6. Adjust the appropriate retransmission timeout by changing the value of the variable `timeout` on line 10 to the optimal time we found previously: ~2 * delay value. Also, adjust the window size by changing the value of the variable `window_size` on line 12. Then, in the window for H1, run
        ```
        python sender.py
        ```
        
    7. Adjust the appropriate delay value in both the bash files. In the terminal window, exit the mininet instance, and repeat steps 3-6.