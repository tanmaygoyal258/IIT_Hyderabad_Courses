#include "types.h"
#include "stat.h"
#include "user.h"

int main()
{
    int array[100];
    // initializing and using the array
    array[0] = 1;
    array[0] += 0;

    printf(1 , "Initial Value is %d\n" , array[0]);

    // forking
    int pid = fork();

    if(pid == 0)
    {// child process
        printf(1 , "Inside child\n");
        mypgtPrint();
        array[0] = 10;
    }

    else
    {// parent process
        printf(1 , "Inside parent\n");
        mypgtPrint();
        array[0] = 20;
    }

    printf(1 , "Final Value is %d\n" , array[0]);

    return 0;

}