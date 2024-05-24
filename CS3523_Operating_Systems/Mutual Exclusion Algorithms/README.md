## This is a README dedicated to Assignment3 of CS3523- Operating Systems- 2

### Author: Tanmay Goyal- AI20BTECH11021

Aim: The goal of this assignment is to implement TAS, CAS and Bounded Waiting with CAS mutual exclusion (ME) algorithms.


1. Enter the directory using the following command: <br />
    ```
    cd <previousDirectories>/ProgAssgn3-AI20BTECH11021
    ```

2. Make sure the previous output file is not present. 
This can be ensured by running the following command: <br />
    ```
    rm out*
    ```

3. Ensure the previous executable file is also deleted using the following command: <br />
    ```
    rm *.out
    ```

4. The folder consists of an input file named `inp-params.txt`, which consists of the following parameters: Number of desired threads, Number of requests to the Critical Section, lambda1, and lambda2, in that order respectively. Lambda1 and lambda2 are the means of the exponential distributions for generating sleep times for the critical section and remainder section respectively. All of these can be adjusted manually.

5. Compile all the three programs using the following commands: <br />
    ```
    g++ -std=c++11 Assgn3-Src-tas-AI20BTECH11021.cpp -o tas.out
    g++ -std=c++11 Assgn3-Src-cas-AI20BTECH11021.cpp -o cas.out
    g++ -std=c++11 Assgn3-Src-cas-bounded-AI20BTECH11021.cpp -o cas-bounded.out
    ```

6. Run all the executable files using:
    ```
    ./ tas.out && ./ cas.out && ./ cas-bounded.out
    ```