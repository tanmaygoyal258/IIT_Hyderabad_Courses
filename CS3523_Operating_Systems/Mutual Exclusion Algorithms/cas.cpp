// importing required libraries
# include <iostream>
# include <unistd.h>
# include <chrono>
# include <cstring>
# include <atomic>
# include <pthread.h>
# include <random>
# include <fstream>

using namespace std;

// defining an atomic flag
atomic<bool> flag {false};

// defining a class to hold the parameters for each thread
class params
{
    public: 
        int K;                  // number of critical section requests
        int thread_number;      // thread number
        double lambda1;         // exponential distribution parameter for critical section time
        double lambda2;         // exponential distribution parameter for remainder section time
        FILE* f;                // file pointer to write to

    // defining the constructor
    params(int K , int thread_number , double lambda1 , double lambda2 , FILE* (f)):
        K(K) , thread_number(thread_number), lambda1(lambda1) , lambda2(lambda2) , f(f)  {}
};

// function declaration for checking the algorithm
void* testCS(void* parameters);

// global variables to hold the average and worst case times of entering the critical section
double avg_time = 0;
double worst_case_time = -1;

int main()
{
    // defining the variables
    int num_threads, num_cs , l1 , l2;

    // name of input file
    string input_file_name = "inp-params.txt";

    // opening input file
    ifstream indata;
    indata.open(input_file_name);

    // if file cannot be opened, return error
    if(!indata){
        cout<< "Error: File not Found!" << endl;
        return 0;
    }

    // reading the number of threads and the side of the sudoku
    indata >> num_threads >> num_cs >> l1 >> l2;

    // closing the input file
    indata.close();

    // opening the output file
    FILE* f = fopen("output_cas.txt" , "w");

    // printing the heading
    fprintf(f , "Summary for Compare and Swap for %d threads and %d Crticial Section Requests\n" , num_threads , num_cs);
    fprintf(f , "\n");

    // defining the array to hold the parameters for each thread
    params* thread_parameters = (params*) malloc(num_threads * sizeof(params));

    // intialising the array
    for(int i = 0 ; i < num_threads ; i++)
        thread_parameters[i] = params(num_cs , i , l1 ,  l2 , f);

    // defining the array to hold the thread ids
    pthread_t t_id[num_threads];

    // creating the threads
    for (int t = 0 ; t < num_threads ; t++)
        // passing the address of the class parameters helps in passing as void*
        pthread_create(&t_id[t] , NULL , testCS , &thread_parameters[t]);

    // waiting for all threads to finish
    for (int t = 0 ; t < num_threads ; t++)
        pthread_join(t_id[t] , NULL);

    // printing the average and worst case times to file and terminal for convinience
    fprintf(f , "\n");
    fprintf(f , "Average time to enter critical section = %f seconds\n" , avg_time / (1000000 * num_threads * num_cs));
    fprintf(f , "Worst case time to enter critical section = %f seconds\n" , worst_case_time / 1000000);
    // cout << "   Compare and Swap" << endl;
    // cout << "Average time to enter critical section = " << avg_time / (1000000 * num_threads * num_cs) << " seconds" << endl;
    // cout << "Worst case time to enter critical section = " << worst_case_time / 1000000 << " seconds" << endl;

    // closing the output file
    fclose(f);

    // freeing the memory on the heap
    free(thread_parameters);

    return 0;
}


void* testCS(void* parameters)
{
    // typecasting the void* to params*
    params* p = (params*) parameters;

    //  retrieving the parameters
    int num_cs = p -> K;
    double l1 = p -> lambda1;
    double l2 = p -> lambda2;
    int id = p -> thread_number;
    FILE* f = p -> f;

    // defining the random generator for exponential distribiution
    unsigned seed =  chrono::system_clock::now().time_since_epoch().count();
    default_random_engine generator (seed);
    exponential_distribution <double> distribution1 (l1);
    exponential_distribution <double> distribution2 (l2);

    for(int i = 0 ; i < num_cs ; i++)
    {        
        // recording and printing the time when request is made
        std::chrono::time_point<std::chrono::system_clock> start = chrono::system_clock::now();
        time_t start_time = std::chrono::system_clock::to_time_t(start);
        
        // generating the time string
        time_t t = time(NULL);
        string s = ctime(&t);
        int colon = s.find(":");
        s = s.substr(colon-2 , 8);
        
        // printing the request time
        fprintf(f , "%d CS request made at %s by thread %d \n" , i + 1 , s.c_str() , id + 1);

        // ENTRY SECTION
        while (1)
        {
            /*
            This definition of the entry section is different from the one given in textbook because of the 
            way the compare_exchange_strong function works. If flag is the same as expected, it replaces flag with new_val. 
            However, what is different is that if flag is not the same as expected, it replaces expected with flag.
            What this means is when the flag has been set to true, and it does not match expected, it replaces 
            expected with true, and then in the next round, a thread will be able to access the critical section.
            Because of this, we keep redefining expected and new_val for every iteration of the loop
            Also, the return value of compare_exchange_strong is not the original value of the flag, it is True
            if the value of flag is changed i.e flag == expected, and False otherwise
            So, it breaks out of the while loop if flag == expected, i.e flag was false.
            In this case, compare_exchange_strong changes flag to true, and thus returns true.
            */
            bool expected = false;
            bool new_val = true;
            if(flag.compare_exchange_strong(expected , new_val)) break;
        }

        // CRITICAL SECTION -> All important write to files and updates to variables would be made here

        // recording and printing time to enter
        std::chrono::time_point<std::chrono::system_clock> enter = chrono::system_clock::now();
        double elapsed1 = std::chrono::duration_cast<std::chrono::microseconds>(enter - start).count();
        fprintf(f , "%d CS entered after %f seconds by thread %d\n" , i + 1 , elapsed1 / 1000000 , id + 1);

        usleep(distribution1(generator) * 1000000); 

        // updating the average and worst_case time
        avg_time += elapsed1;
        if(elapsed1 > worst_case_time) worst_case_time = elapsed1;

        // recording the time when exit is made
        std::chrono::time_point<std::chrono::system_clock> exit = chrono::system_clock::now();
        double elapsed2 = std::chrono::duration_cast<std::chrono::microseconds>(exit - start).count();
        fprintf(f , "%d CS exiting after %f seconds by thread %d\n" , i + 1 , elapsed2 / 1000000 , id + 1);

        // EXIT SECTION
        flag = false;

        // REMAINDER SECTION
        usleep(distribution2(generator) * 1000000);
    }
    return NULL;
}