#include "types.h"
#include "stat.h"
#include "user.h"

#define N 3000
int glob[N];

int main(){

    // randomly initializing with any value
    glob[0] = 2;

    printf(1 , "Global address from User space: %x\n" , glob);


    for(int i = 1 ; i < N ; i++){
        glob[i] = glob[i-1];
        if (i%1000 == 0) mypgtPrint();
    }

    printf(1 , "Printing final page table \n");
    mypgtPrint();

    printf(1 , "The final value in glob is %d\n" , glob[N-1]);

    exit();
}