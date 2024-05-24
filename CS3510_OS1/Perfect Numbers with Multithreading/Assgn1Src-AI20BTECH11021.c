# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <pthread.h>


// function declaration 
int perfect_number(int n);
void* thread_check_perfect_number(void* arr);

// to store the perfect numbers found
int results[200];
int offset = 0;

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
    // and one additional columns to show number of columns
    int rows = K;
    int columns;
    columns = N/K + 1;

    // declaring the 2D array for division of numbers
    // note that for every row, the first element is the thread number
    // note that for every row, the second element is number of columns
    int division[rows][columns];
    for(int i = 0 ; i < rows ; i++)
    {
        for(int j = 0 ; j < columns ; j++)
        {
            int number;
            if (j==0) number = i + (j * rows) + 1;
             // putting the number of columns for easy access
            else if (j == 1) number = columns;             
            else number = i + ((j - 1) * rows) + 1;
            if(number > N) division[i][j] = -1; // number is not present
            else division[i][j] = number;
        }
    }

    // declaring array for thread-ids
    pthread_t t_id[K];

    
    for (int t = 0 ; t < K ; t++)
        pthread_create(&t_id[t] , NULL , thread_check_perfect_number , division[t]);

     for (int t = 0 ; t < K ; t++)
        pthread_join(t_id[t] , NULL);


    // opening the parent output file
    char* filename = "OutMain.txt";
    f = fopen(filename , "w");
    fprintf(f , "Perfect Numbers identified between 1 and %d:\n\n" , N);

    for(int i = 0 ; i < offset ; i += 2)
    {
        fprintf(f , "Process %d : %d \n" , results[i+1] , results[i]);
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

void* thread_check_perfect_number(void* arr){
    /*
    This is the function that will be executed by each thread. 
    This will check if the set of allotted numbers are perfect numbers and 
    write accordingly to the file.
    */

    int* array = (int*) arr;

    // opening the file to write
    char filename[20] = "OutFile";
    char extension[20] = ".txt";
    char thread_num[12];

    // to convert integer to string
    sprintf(thread_num , "%d" , array[0]);
    strcat(filename , thread_num);
    strcat(filename , extension);
    
    // opening the file to write
    FILE* f = fopen(filename , "w");
    fprintf(f , "Thread Number %d\n\n" , array[0]);

    int columns = array[1];

    for(int i = 0 ; i < columns ; i++)
        {
            if (i == 1) continue;   // because the second element is number of columns

            int num = array[i];

            if (num > 0) 
            {   
                // it is a valid assigned number

                if(perfect_number(num))
                {
                    // printing to the file
                    fprintf(f , "%d: Is a perfect number\n" , num);

                    //storing results in the global space
                    results[offset] = num;
                    results[offset + 1] = array[0];

                    // increasing offset by 2
                    offset+=2;

                }
                // if not a perfect number, writing to the file
                else fprintf(f , "%d: Not a perfect number\n",num);
            }
        }
    // closing the file
    fclose(f);

    return NULL;
}


