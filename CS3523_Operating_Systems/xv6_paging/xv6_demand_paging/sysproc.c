#include "types.h"
#include "x86.h"
#include "defs.h"
#include "date.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"

int
sys_fork(void)
{
  return fork();
}

int
sys_exit(void)
{
  exit();
  return 0;  // not reached
}

int
sys_wait(void)
{
  return wait();
}

int
sys_kill(void)
{
  int pid;

  if(argint(0, &pid) < 0)
    return -1;
  return kill(pid);
}

int
sys_getpid(void)
{
  return myproc()->pid;
}

int
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = myproc()->sz;
  if(growproc(n) < 0)
    return -1;
  return addr;
}

int
sys_sleep(void)
{
  int n;
  uint ticks0;

  if(argint(0, &n) < 0)
    return -1;
  acquire(&tickslock);
  ticks0 = ticks;
  while(ticks - ticks0 < n){
    if(myproc()->killed){
      release(&tickslock);
      return -1;
    }
    sleep(&ticks, &tickslock);
  }
  release(&tickslock);
  return 0;
}

// return how many clock tick interrupts have occurred
// since start.
int
sys_uptime(void)
{
  uint xticks;

  acquire(&tickslock);
  xticks = ticks;
  release(&tickslock);
  return xticks;
}

int sys_mydate(){

struct rtcdate *r;
if(argptr(0 , (void*)&r , sizeof(r)) < 0) return -1;
  cmostime(r);
  return 0;
}

int sys_mypgtPrint(){
  // REFERENCE FROM freevm() IN vm.c
  pde_t* pagedir = myproc()->pgdir;
  int counter = 0;
  // for each entry in the page directory
  for(int i = 0 ; i < NPDENTRIES ; i++){

    if(pagedir[i] & PTE_P) {
    char* v = P2V(PTE_ADDR(pagedir[i]));
    pde_t* pagetable = (pde_t *) v;
      for(int j = 0 ; j < NPTENTRIES ; j++){
        uint valid_bit = pagetable[j] & PTE_P;
        uint user_bit = pagetable[j] & PTE_U;

        if (valid_bit && user_bit)
        {cprintf("Entry Number: %d, Virtual Address: %p , Physical Address: %x\n" ,
                                                             counter , P2V(pagetable[j]) , pagetable[j]);
         counter++;

        }
      }     
    }
  }
  return 0;
}