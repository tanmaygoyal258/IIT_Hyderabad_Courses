// importing required libraries
# include <iostream>
# include <fstream>
# include <math.h>
# include <chrono>
# include <pthread.h>

using namespace std;

// function declaration
void* check_sudoku(void* str);

// since the maximum size of the board will be 100 x 100
// we will require 300 checks, 100 rows, 100 columns and 100 grids
# define MAX_CHECKS 300

// this array will store the result of each check -> 0 if invalid and 1 if valid
int result_thread[MAX_CHECKS];

// defining a class to hold the parameters for each thread
class params
{
    public: 
        int N;                  // size of the sudoku 
        int total_threads;      // total number of threads we are creating -> helps in dividing the work
        int thread_num;         // the thread_number
        int** sudoku;           // the pointer to the sudoku board

    params(int N , int total_threads , int thread_num , int** sudoku):
        N(N) , total_threads(total_threads) , thread_num(thread_num) , sudoku(sudoku) {}

};


int main(){
    
    // creating variables for the number of threads and the side of the sudoku
    int number_of_threads_original , N;

    // name of input file
    string input_file_name = "input.txt";

    // opening input file
    ifstream indata;
    indata.open(input_file_name);

    // if file cannot be opened, return error
    if(!indata){
        cout<< "Error: File not Found!" << endl;
        return 0;
    }

    // reading the number of threads and the side of the sudoku
    indata >> number_of_threads_original >> N;
    
    // creating our sudoku board
    int** sudoku = new int*[N];
    for(int i = 0 ; i < N ; i++) sudoku[i] = new int[N];

    // retrieving the elements of the sudoku board
    for(int i = 0 ; i < N ; i++)
    {
        for(int j  = 0 ; j < N ; j++)
        {
            indata >> sudoku[i][j];
        }
    }

    // closing the input file
    indata.close();


    /*
    declaring another variable for number of threads
    we replace the number of threads with 3 * N if the number of threads is greater than 3 * N
    this is because we have a total of 3 * N tasks
    each task is not broken down further 
    */
    int number_of_threads = number_of_threads_original;
    if(number_of_threads_original >= 3 * N) number_of_threads = 3 * N;
    

    // defining an array for the thread parameters
    params* thread_parameters = (params*) malloc(number_of_threads * sizeof(params));

    // intialising the array
    for(int i = 0 ; i < number_of_threads ; i++)
        thread_parameters[i] = params(N , number_of_threads , i , sudoku);

    // starting the timer
    auto start_time = std::chrono::high_resolution_clock::now();    

    // defining an array to store the thread ids
    pthread_t t_id[number_of_threads];

    // creating the threads
    for (int t = 0 ; t < number_of_threads ; t++)
        // passing the address of the class parameters helps in passing as void*
        pthread_create(&t_id[t] , NULL , check_sudoku , &thread_parameters[t]);

    // waiting for all threads to finish
    for(int t = 0 ; t < number_of_threads ; t++)    
        pthread_join(t_id[t] , NULL);

    // ending the timer
    auto end_time = std::chrono::high_resolution_clock::now();
    
    // opening the output file
    ofstream outdata;
    outdata.open("output_pthreads.txt");

    // if file cannot be opened, return error
    if(!outdata){
        cout<<"Error: Cannot open file!";
        return 0;
    }

    
    // printing the heading
    outdata << "Report for " << number_of_threads_original << " threads and a sudoku of size " << 
        N << " x " << N << "\n";
        
    
    // the total number of tasks is 3 * N -> helps to create a bound for the iteration pover result_threads
    int number_tasks = 3 * N;

    // will store the sum of entries in results_thread
    // if not equal to 3 * N, there was some 0 encountered, i.e one of the checks was invalid
    int sum = 0;

    // calculating the time taken for creation of threads and the thread processes
    float time_elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time).count();


    for(int i = 0 ; i < number_tasks ; i++)
    {
        /*
        we assume every task to be numbered
        tasks in [0,N) are row checks
        tasks in [N,2N) are column checks
        tasks in [2N,3N) are grid checks
        we use this to determine the thread number -> can also be done using repeated subtraction 
        */
        int thread_num = i % number_of_threads;
        
        // to hold the result of each check
        string result;
        
        sum += result_thread[i];

        // determining the result of each check as a string
        if (result_thread[i] == 1) result = "valid";
        else result = "invalid";

        // printing the result of each check based on the type and validity of the check
        if (i < N) 
            outdata << "Thread " << thread_num << " checks row " << i << " and it is " << result << "\n";
        else if (i < 2 * N) 
            outdata << "Thread " << thread_num << " checks column " << i - N << " and it is " << result << "\n";
        else
            outdata << "Thread " << thread_num << " checks grid " << i - 2*N << " and it is " << result << "\n";

    }

    // since we had a maximum of 3 * N tasks, we could have a maximum of 3 * N threads
    // we print the number of unused threads
    if (number_of_threads_original > number_of_threads) 
        outdata << "\n" << number_of_threads_original - number_of_threads << " threads were unused.\n";

    // printing the output of the entire sudoku
    // if sum is not equal to 3 * N, a 0 was encountered, i.e some check was invalid
    if(sum == 3 * N) 
        outdata << "\nThe Suduko Solution is valid.\n";
    else 
        outdata << "\nThe Suduko Solution is invalid.\n";
    
    // printing the duration
    outdata << "\nThe time taken is " << time_elapsed << " microseconds \n";

    // closing the output file
    outdata.close();

    return 0;
}


void* check_sudoku(void* str){

    // converting the void* argument back into a params* pointer
    params* parameters = (params*) str;

    // extracting the required values from the struct
    int N = parameters->N;
    int start = parameters -> thread_num;

    // number of tasks required to be check ->  N rows,  N columns, N grids
    int number_checks = 3 * N;
    
    /* 
    we assume our tasks our numbered
    tasks in [0,N) are row checks
    tasks in [N,2N) are column checks
    tasks in [2N,3N) are grid checks
    start will determine the task number, and then we check if it is a row, column or grid check
    we keep adding the number of threads to start to check if there is a next task
    in case the number of threads is less than the number of tasks
    */
    while(start < number_checks)
    {
        if (start < N) 
        {
            // perform row check with row_number = start
            int row = start;

            // distinct array to check if all numbers are distinct
            int distinct[N];

            // valid or invalid check
            int result = 1;
            
            // setting all elements of distinct to 0
            for(int i = 0 ; i < N ; i++)
            {
                distinct[i] = 0;
            }

            // checking over the row
            for(int i = 0 ; i < N ; i++)
            {
                
                // extracting the number
                int number = parameters->sudoku[row][i];

                // if the distinct array has not seen the number before (distinct array is set to 0)
                // change it to 1
                if (distinct[number-1] == 0) distinct[number-1] = 1;
                
                else {  
                    // we have a repeating number, i.e the row is invalid
                    result = 0;
                    break;
                }
            }

            // update the result_thread array with the result of this check
            result_thread[start] = result;

        }
        else if (start < 2 * N)
        {
            // perform column check with column_number = start - N
            int col = start - N;

            // distinct array to check if all numbers are distinct
            int distinct[N];

            // valid or invalid check
            int result = 1;
            
            // setting all elements of distinct to 0
            for(int i = 0 ; i < N ; i++)
            {
                distinct[i] = 0;
            }

            // checking over the column
            for(int i = 0 ; i < N ; i++)
            {
                
                // extracting the number
                int number = parameters->sudoku[i][col];

                // if the distinct array has not seen the number before (distinct array is set to 0)
                // change it to 1
                if (distinct[number-1] == 0) distinct[number-1] = 1;
                
                else
                {  
                    // we have a repeating number, i.e the column is invalid
                    result = 0;
                    break;
                }
            }

            // update the result_thread array with the result of this check
            result_thread[start] = result;

        }
        else
        {
            // perform a grid check with grid_number = start - 2 * N
            int grid_num = start - 2 * N;

            // the number of grids in each row or column = sqrt(N)
            int sqrt_sudoku = sqrt(N);

            /* 
            calculating the starting row and column for the grid
            note that the denominator and multiplicand donot cancel out
            this is because we are doing integer division
            example 4 * (5/4) is not 5 because 5/4 is not 1.75 but 1
            */
            int start_row = sqrt_sudoku * (grid_num / sqrt_sudoku);
            int start_col = sqrt_sudoku * (grid_num % sqrt_sudoku);

            // distinct array to check if all numbers are distinct
            int distinct[N];

            // valid or invalid check
            int result = 1;

            // setting all elements of distinct to 0
            for(int i = 0 ; i < N ; i++)
            {
                distinct[i] = 0;
            }
            
            // checking over the grid   
            for(int i = start_row ; i < start_row +sqrt_sudoku ; i++)
            {
                for(int j = start_col ; j < start_col + sqrt_sudoku ; j++)
                {
                    
                    // extracting the number
                    int number = parameters->sudoku[i][j];
                    
                    // if the distinct array has not seen the number before (distinct array is set to 0)
                    // change it to 1
                    if (distinct[number-1] == 0) distinct[number-1] = 1;
                    
                    else 
                    {  
                        // we have a repeating number, i.e the grid is invalid
                        result = 0;
                        break;
                    }
                }
            }

            // update the result_thread array with the result of this check
            result_thread[start] = result;
        }

        // incrementing start by the number of threads to go to the next task
        start += parameters -> total_threads;
    }   

    // since return type is void*
    return NULL;
}