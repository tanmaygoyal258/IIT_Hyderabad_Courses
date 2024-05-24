// Physical memory allocator, intended to allocate
// memory for user processes, kernel stacks, page table pages,
// and pipe buffers. Allocates 4096-byte pages.

#include "types.h"
#include "defs.h"
#include "param.h"
#include "memlayout.h"
#include "mmu.h"
#include "spinlock.h"

#define MAXPAGES PHYSTOP/PGSIZE

void freerange(void *vstart, void *vend);
extern char end[]; // first address after kernel loaded from ELF file
                   // defined by the kernel linker script in kernel.ld

struct run {
  struct run *next;
};

struct {
  struct spinlock lock;
  int use_lock;
  struct run *freelist;

  // an integer array to keep track of the number of references to each page
  // we wish to keep it locked under kmem because multiple processes might request for memory
  uint page_references[MAXPAGES];
} kmem;

// Initialization happens in two phases.
// 1. main() calls kinit1() while still using entrypgdir to place just
// the pages mapped by entrypgdir on free list.
// 2. main() calls kinit2() with the rest of the physical pages
// after installing a full page table that maps them on all cores.
void
kinit1(void *vstart, void *vend)
{
  initlock(&kmem.lock, "kmem");
  kmem.use_lock = 0;
  freerange(vstart, vend);
}

void
kinit2(void *vstart, void *vend)
{
  freerange(vstart, vend);
  kmem.use_lock = 1;
}

void
freerange(void *vstart, void *vend)
{
  char *p;
  p = (char*)PGROUNDUP((uint)vstart);
  for(; p + PGSIZE <= (char*)vend; p += PGSIZE)
  {
    kfree(p);

    // initialize all entries of the array to zero
    kmem.page_references[V2P(p) / PGSIZE] = 0;
  }
}
//PAGEBREAK: 21
// Free the page of physical memory pointed at by v,
// which normally should have been returned by a
// call to kalloc().  (The exception is when
// initializing the allocator; see kinit above.)
void
kfree(char *v)
{
  struct run *r;

  if((uint)v % PGSIZE || v < end || V2P(v) >= PHYSTOP)
    panic("kfree");


  if(kmem.use_lock)
    acquire(&kmem.lock);
  
  r = (struct run*)v;
  
  // if the page has more than one reference, we can't free it
  if (kmem.page_references[V2P(v) / PGSIZE] > 1)
    kmem.page_references[V2P(v)/PGSIZE] -= 1;

  else
  { // references were 1, so now we can decrease it and free the page

    // Fill with junk to catch dangling refs.
    memset(v, 1, PGSIZE);
    kmem.page_references[V2P(v)/PGSIZE] = 0;
    r->next = kmem.freelist;
    kmem.freelist = r;
  }
  
  if(kmem.use_lock)
    release(&kmem.lock);
}

// Allocate one 4096-byte page of physical memory.
// Returns a pointer that the kernel can use.
// Returns 0 if the memory cannot be allocated.
char*
kalloc(void)
{
  struct run *r;

  if(kmem.use_lock)
    acquire(&kmem.lock);
  r = kmem.freelist;
  if(r)
  {
    kmem.freelist = r->next;

    // set the number of references to the page as 1
    kmem.page_references[V2P((char*)r) /PGSIZE] = 1;
  }
  if(kmem.use_lock)
    release(&kmem.lock);
  return (char*)r;
}

void increase_ref(uint pa)
{
  // acquire the lock
  if (kmem.use_lock) acquire(&kmem.lock);

  // increase the references
  kmem.page_references[pa / PGSIZE] += 1;

  // release the lock
  if(kmem.use_lock) release(&kmem.lock);
}

void decrease_ref(uint pa)
{
  // acquire the lock
  if (kmem.use_lock) acquire(&kmem.lock);

  // decrease the references
  kmem.page_references[pa / PGSIZE] -= 1;

  // release the lock
  if(kmem.use_lock) release(&kmem.lock);
}

int get_ref(uint pa)
{
  return kmem.page_references[pa/PGSIZE];
}

