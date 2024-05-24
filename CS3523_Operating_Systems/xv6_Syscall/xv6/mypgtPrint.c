# include "types.h"
# include "date.h"
# include "user.h"

// uncomment to check with Global Array
// int arrGlobal[10000];

int main(){
    // uncomment to check with Global Array
    // printf(2 , "When a global array has been declared, the page table entries look like: \n");
    
    // uncomment to check with Local Array
    int arrLocal[10000];
    arrLocal[0] = 1;
    arrLocal[0] += 1;
    printf(2 , "When a local array has been declared, the page table entries look like: \n");

    
    mypgtPrint();
    exit();
}