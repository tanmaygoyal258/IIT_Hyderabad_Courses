# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/wait.h>
# include <unistd.h>
# include <fcntl.h>
# include <sys/mman.h>


// function declaration 
int perfect_number(int n);


int main()
{
    
    // opening the input file
    FILE * f = fopen("input.txt" , "r");
    if(!f)
    {
        printf("Error opening input file.");
        return 0;
    }

    // reading the values of N and K from the input file
    int N , K;
    fscanf(f , "%d %d" , &N , &K);
    
    // closing the input file
    fclose(f);

    // checking for validity of N and K
    if(N <= 0 || K <= 0)
    {
        printf("Invalid Input");
        return 0;
    }

    // declaring rows and columns for convinience
    // we will divide the numbers in K rows and N/K columns 
    int rows = K;
    int columns;
    if(N % K == 0) columns = N / K;
    else columns = (N / K) + 1;

    // declaring the 2D array for division of numbers
    int division[rows][columns];
    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0 ; j < columns ; j++)
        {
            int number = i + (j * rows) + 1;
            if(number > N) division[i][j] = -1; // number is not present
            else division[i][j] = number;
        }
    }


    // declaring two shared memories
    // 1. for storing all the perfect numbers found
    // 2. for storing the offset for the pointer to the first shared memory
    int shm_fd1;
    int size1 = 4096;
    int *ptr1;
    char name1[] = "SharedMemory1";
    shm_fd1 = shm_open(name1 , O_CREAT | O_RDWR , 0666);
    ftruncate(shm_fd1 , size1);
    ptr1 = mmap(0 , size1 , PROT_WRITE , MAP_SHARED , shm_fd1 , 0);

    int shm_fd2;
    int size2 = 4;
    int *ptr2;
    char name2[] = "SharedMemory2";
    shm_fd2 = shm_open(name2 , O_CREAT | O_RDWR , 0666);
    ftruncate(shm_fd2 , size2);
    ptr2 = mmap(0 , size2 , PROT_WRITE , MAP_SHARED , shm_fd2 , 0);
    
    // initially, base index is zero
    ptr2[0] = 0;
                
    pid_t pid;

    // creating K child processes
    for(int process = 0 ; process < K ; process++)
    {
        pid = fork();
        
        if(pid < 0)
        {
            printf("Error while Forking \n");
            return 0;
        }

        else if(pid == 0)
        { 
            // it is a child process
        
            // creating the output file name
            char filename[20] = "OutFile";
            char extension[20] = ".txt";
            char process_number[12];

            // to convert integer to string
            sprintf(process_number , "%d" , process + 1);
            strcat(filename , process_number);
            strcat(filename , extension);
            
            // opening the file to write
            FILE* f = fopen(filename , "w");
            fprintf(f , "Process Number %d\n\n" , process+1);

            // opening the children's connections to both the shared memory
            int shm_fd1 =  shm_open(name1 , O_RDWR , 0666);
            ftruncate(shm_fd1 , size1);
            ptr1 = mmap(0 , size1 , PROT_WRITE , MAP_SHARED , shm_fd1 , 0);

            int shm_fd2 =  shm_open(name2 , O_RDWR , 0666);
            ftruncate(shm_fd2 , size2);
            ptr2 = mmap(0 , size2, PROT_WRITE , MAP_SHARED , shm_fd2 , 0);

            // checking if the number assigned to the process is a perfect number or not
            for(int i = 0 ; i < columns ; i++)
            {
                int num = division[process][i];

                if (num > 0) 
                {   
                    // it is a valid assigned number

                    if(perfect_number(num))
                    {
                        // printing to the file
                        fprintf(f , "%d: Is a perfect number\n" , num);

                        // in the first shared memory, storing the number 
                        // and the process that identified it 
                        ptr1[ptr2[0]] = num;
                        ptr1[ptr2[0] + 1] = process + 1;

                        // in the second shared memory, incrementing the offset by 2
                        ptr2[0]+=2;

                    }
                    // if not a perfect number, writing to the file
                    else fprintf(f , "%d: Not a perfect number\n",num);
                }
            }
            // closing the file
            fclose(f);

            // making sure the child process exits, else it will keep looping
            exit(0);
        }
    }

    // making sure the parent process waits for all K child processes to finish
    for(int i = 0 ; i < K ; i++)
    {
        wait(NULL);
    }

    // opening the parent output file
    char* filename = "OutMain.txt";
    f = fopen(filename , "w");
    fprintf(f , "Perfect Numbers identified between 1 and %d:\n\n" , N);

    // checking in the first shared memory to retrieve all perfect numbers and their processes
    // the integer in the second shared memory tells us when to terminate the loop
    // i gets incremented by 2, because we have a pair of perfect number and process
    for(int i = 0 ; i < ptr2[0] ; i += 2)
    {
        fprintf(f , "Process %d : %d \n" , ptr1[i+1] , ptr1[i]);
    }

    // closing the file
    fclose(f);

    return 0;
}


int perfect_number(int n){
/*
    This function checks if a given number n, is a perfect number or not.
    Parameters: n -> the number to be checked
    Returns: 1 if n is a perfect number, 0 otherwise    
*/
    int sum = 0;
    for(int i = 1 ; i < n ; i++)
    {
        if (n % i == 0) sum += i;   
        if (sum > n) return 0;  
    }

    if (sum == n) return 1;
    else return 0;
}


