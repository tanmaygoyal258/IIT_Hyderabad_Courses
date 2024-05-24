## This is a README dedicated to the Final Exam of CS3523- Operating Systems- 2

### Author: Tanmay Goyal- AI20BTECH11021

Aim: To implement FIFO, LRU and OPT page replacement policies


1. Enter the directory using the following command: <br />
    ```
    cd prevDir/LabExam-PageRepPolicy-<AI20BTECH11021>
    ```
2. The folder consists of an input file named `input.txt`, which consists of the number of physical frames, the page size in bytes, and the addresses that are accesed by the CPU. Note that, to signify the end of the input, I have used -1 as an EOF character. Please keep this in mind while entering inputs 

3. Ensure the previous executable file is also deleted using the following command: <br />
    ```
    rm *.out
    ```

4. Compile the program using the following command: <br />
    ```
    g++ -std=c++11 PageReplacement.cpp -o code.out

    ```

5. Run the executable File using:
    ```
    ./code.out
    ```