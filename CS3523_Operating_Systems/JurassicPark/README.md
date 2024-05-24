## This is a README dedicated to Assignment4 of CS3523- Operating Systems- 2

### Author: Tanmay Goyal- AI20BTECH11021

Problem Statement: Jurassic Park consists of a dinosaur museum and a park for safari riding.
There are m passengers and n single-passenger cars. Passengers wander around the museum
for a while, then line up to take a ride in a safari car. When a car is available, it loads the one passenger it can hold and rides around the park for a random amount of time. If the n cars are all out riding passengers around, then a passenger who wants to ride waits; if a car is ready to load, but there are no waiting passengers, then the car waits. Use semaphores to synchronize the m-passenger processes and the n-car processes.

NOTE: this was run on a Linux based system, and not on Mac because Mac does not support unnamed semaphores. This issue can be resolved by using sem_open and sem_close for named semaphores instead of sem_init and sem_destroy.

1. Enter the directory using the following command: <br />
    ```
    cd <previousDirectories>/ProgAssgn4-AI20BTECH11021
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

4. The folder consists of an input file named `inp-params.txt`, which consists of the following parameters: Number of passenger threads, NUmber of car threads , lambda_p , lambda_c and the Number of requests per passenger in that order respectively. Lambda_p and lambda2_c are the means of the exponential distributions for generating the wait times between two requests of a passenger and two successive rides of a car respectively. All of these can be adjusted manually.

5. Compile all the three programs using the following commands: <br />
    ```
    g++ -std=c++11 Assgn4-Src-AI20BTECH11021.cpp -o JP.out
    ```

6. Run all the executable files using: <br />
    ```
    ./JP.out
    ```

7. In case you run into an error that looks like the one shown below, then simply repeat steps 5 and 6. <br />
  ```
  terminate called after throwing an instance of 'std::out_of_range'
  what():  basic_string::substr: __pos (which is 18446744073709551613) > this->size() (which is 0)
  Aborted (core dumped)
  ```
  