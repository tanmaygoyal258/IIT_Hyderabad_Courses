## This is a README dedicated to Assignment2 of CS3523- Operating Systems- 2

### Author: Tanmay Goyal- AI20BTECH11021

Aim: To develop a multi-threaded program validate a Sudoku of given size using PThreads and OpenMP, and compare the performance of both.

NOTE: this was implemented on a Linux based system, and not on Mac. This is due to the easy support for OpenMP on Linux.

1. Enter the directory using the following command: <br />
    ```
    cd <previousDirectories>/Assgn2_AI20BTECH11021
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

4. Generate the input file using the python script `sudoku_generator.py`. We also mention the number of threadas and the size of the sudoku. For example, to generate an input file with 16 threads and a 49 x 49 sudoku board is: <br />
    ```
    python3 sudoku_generator.py 16 49
    ```

5. Compile the PThreads program using the following command: <br />
    ```
    g++ -std=c++11 Assgn2Srcpthread_AI20BTECH11021.cpp -o pthread.out

    ```

6. Compile the OpenMP program using the following command: <br />
    ```
    g++ -std=c++11 Assgn2SrcOpenMp_AI20BTECH11021.cpp -fopenmp -o openmp.out

    ```
    Note the use of `-fopenmp` flag. This is to ensure the OpenMP library gets linked.

7. Run the executable files using:
    ```
    ./pthread.out
    ./openmp.out
    ```