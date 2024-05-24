# include "types.h"
# include "date.h"
# include "user.h"


// int arrGlobal[10000];

int main(){
    // printf(2 , "When a global array has been declared, the page table entries look like: \n");
    // int arrLocal[10000];

    // randomly initialzing with values to prevent warnings
    // arrLocal[0] = 1;
    // arrLocal[0] += 1;
    // printf(2 , "When a local array has been declared, the page table entries look like: \n");
    mypgtPrint();
    exit();
}