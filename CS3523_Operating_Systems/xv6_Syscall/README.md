## This is a README dedicated to Assignment5 of CS3523- Operating Systems- 2

### Author: Tanmay Goyal- AI20BTECH11021

Problem Statement:  Syscall Implementation in xv6

NOTE: this was run on a Linux based system. I was unable to run it on a Mac because Linux-ARM arch is unable to support some of the dependencies required for supporting xv6.

<h3> <u>Setting up xv6</u> </h3>

1. Run the following sets of commands: <br />
    ```
    sudo apt-get install qemu qemu-system g++-multilib git-all grub2 grub-pc-bin libsdl-console-dev

    git clone https://github.com/mit-pdos/xv6-public xv6

    cd xv6

    make 

    make qemu-nox
    ```

<h3> <u> Part 1: Understanding and tracing system calls </u> </h3>

1. Go to the file `syscall.c` and <b>uncomment</b> line 175, namely:
```
    cprintf("%s: %s->%d->%d\n" , curproc->name , sysCallNames[num-1] , num , curproc->tf->eax);
```
2. You should be able to see the following output on booting xv6:
```
...
init: write->16->1
init: fork->1->2
sh: exec->7->0
sh: open->15->3
sh: close->21->0
$sh: write->16->1
 sh: write->16->1
```

<h3> <u> Part 2:Implementing your own system call: date </u> </h3>

1. Changes have been made to the following files: `mydate.c` , `sysproc.c` , `syscall.c` , `syscall.h` , `user.h` , `Makefile` , `usys.S`
2. On entering the command `mydate` in xv6, the output should be visible:
```     
---UTC---
Year : 2023
Month : 4 or April
Date : 6
The time is 12:48:51
---IST---
Year : 2023
Month : 4 or April
Date : 6
The time is 18:18:51
```

<h3> <u> Part 3: Printing Page Table entries </u> </h3>

1. Changes have been made to the following files: `mypgtPrint.c` , `sysproc.c` , `syscall.c` , `syscall.h` , `user.h` , `Makefile` , `usys.S`

2. Make sure line 6, line 10 and lines 13-16 in `mypgtPrint.c` are commented out (more on it in the subsequent points). On entering the command `mypgtPrint` in xv6, the output should be visible:
```
Entry Number: 0, Virtual Address: 8df2c027 , Physical Address: df2c027  
Entry Number: 1, Virtual Address: 8df74067 , Physical Address: df74067
```

3. To obtain the page table entries for global array, <b>uncomment</b> line 6 and line 10 in `mypgtPrint.c` and comment out lines 13-16, namely:
```
    int arrGlobal[10000];
    printf(2 , "When a global array has been declared, the page table entries look like: \n");

    // int arrLocal[10000];
    // arrLocal[0] = 1;
    // arrLocal[0] += 1;
    // printf(2 , "When a local array has been declared, the page table entries look like: \n");

```
Lines 14 and 15 were included to avoid unintialized and unused warnings(treated as errors in xv6).

4. To obtain the page table entries for local array, <b>comment out</b> line 6 and line 10 in `mypgtPrint.c` and uncomment lines 13-16, namely:
```
    // int arrGlobal[10000];
    // printf(2 , "When a global array has been declared, the page table entries look like: \n");

    int arrLocal[10000];
    arrLocal[0] = 1;
    arrLocal[0] += 1;
    printf(2 , "When a local array has been declared, the page table entries look like: \n");

```