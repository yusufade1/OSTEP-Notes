---
type: mechanism
source: "OSTEP Ch. 14: Interlude: Memory API"
tags:
  - virtualization
  - memory
  - bugs
related:
  - "[[malloc and free Manage Heap Memory Dynamically]]"
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
  - "[[Memory Virtualization Goals - Transparency Efficiency and Protection]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[malloc and free Manage Heap Memory Dynamically]]"
---

# Common Memory Bugs - Dangling Pointers Double Free and Leaks

> [!SUMMARY]
> Manual memory management in C introduces several categories of bugs: forgetting to allocate, buffer overflows, dangling pointers (use-after-free), double frees, memory leaks, and incorrect use of `free()`. These bugs are notoriously difficult to detect because they often produce no immediate crash—instead corrupting data silently or manifesting far from the original error.

## Forgetting to Allocate

Using a pointer without first allocating the memory it should point to:

```c
char *src = "hello";
char *dst;          // uninitialized pointer
strcpy(dst, src);   // segfault or silent corruption
```

The fix is to allocate `dst` before use with [[malloc and free Manage Heap Memory Dynamically|malloc]]: `char *dst = malloc(strlen(src) + 1);`

## Buffer Overflow

Allocating too little memory and writing beyond the allocated region:

```c
int *array = (int *) malloc(9 * sizeof(int));
array[9] = 0;  // writes past the end of the allocation
```

This overwrites the allocator's internal metadata or adjacent heap objects. The corruption may not manifest until much later when `malloc()` or `free()` reads the damaged metadata—making these bugs extremely hard to localize.

## Dangling Pointer (Use-After-Free)

Freeing memory and then continuing to use the pointer:

```c
int *p = (int *) malloc(sizeof(int));
*p = 42;
free(p);
printf("%d\n", *p);  // undefined behavior
```

After `free(p)`, the allocator may reuse that memory for a subsequent `malloc()`. Reading or writing through the dangling pointer now corrupts unrelated data. The program may appear to work until the freed region is reallocated, making this bug timing-dependent and non-deterministic.

## Double Free

Calling `free()` on the same pointer twice:

```c
int *p = (int *) malloc(sizeof(int));
free(p);
free(p);  // undefined behavior — corrupts free list
```

The second `free()` corrupts the allocator's internal free list. This can cause future `malloc()` calls to return overlapping regions, leading to subtle data corruption across unrelated parts of the program.

## Memory Leak

Allocating memory but never freeing it:

```c
void process_data() {
    int *data = (int *) malloc(1000 * sizeof(int));
    // ... use data ...
    return;  // forgot to call free(data)
}
```

For short-lived programs, leaks are harmless—the OS reclaims all [[The Address Space Abstracts Physical Memory for Each Process|process memory]] on exit. For long-running processes (servers, daemons), leaked memory accumulates until the system runs out of physical memory or swap space, eventually causing allocation failures or the OS killing the process.

## Calling free Incorrectly

Passing an invalid value to `free()`—such as a pointer to stack memory or an offset into a heap allocation—causes undefined behavior:

```c
int x = 5;
free(&x);  // freeing stack memory — undefined

int *p = malloc(100);
free(p + 10);  // freeing interior pointer — undefined
```

## Detection Tools

Because these bugs often produce no immediate visible error, specialized tools exist to detect them:

- **Valgrind (memcheck):** Instruments every memory access to catch leaks, use-after-free, and overflows at runtime.
- **AddressSanitizer (ASan):** Compiler instrumentation that detects buffer overflows and use-after-free with lower overhead than Valgrind.
- **Purify, Electric Fence:** Earlier tools that surrounded allocations with guard pages or tracking metadata.

These tools trade performance for safety during development and testing, catching bugs that would otherwise remain latent until production.
