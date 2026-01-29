---
type: mechanism
source: "OSTEP Ch. 14: Interlude: Memory API"
tags:
  - virtualization
  - memory
  - api
related:
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
  - "[[Common Memory Bugs - Dangling Pointers Double Free and Leaks]]"
  - "[[A Process is a Running Program]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[Stack and Heap Occupy Opposite Ends of the Address Space]]"
---

# malloc and free Manage Heap Memory Dynamically

> [!SUMMARY]
> The C library functions `malloc()` and `free()` provide the programmer's interface to heap memory. `malloc()` allocates a block of the requested size and returns a pointer to it; `free()` releases a previously allocated block. These are library calls—not system calls—that manage a user-space free list, occasionally requesting more memory from the OS via `brk()` or `mmap()`.

## malloc: Requesting Heap Memory

The `malloc()` function takes a single argument—the number of bytes needed—and returns a `void*` pointer to the allocated region:

```c
#include <stdlib.h>

int *array = (int *) malloc(10 * sizeof(int));
if (array == NULL) {
    // allocation failed — out of memory
    exit(1);
}
```

Key details:

- The argument is the **size in bytes**, not the number of elements. Using `sizeof()` ensures portability across architectures with different type sizes.
- `malloc()` returns `NULL` on failure—always check the return value.
- The returned memory is **uninitialized**; it contains whatever bytes were previously at that location. Use `calloc()` if zero-initialization is needed.
- `malloc()` is a **library function**, not a system call. It manages an internal free list and only calls the OS (via `brk()` or `mmap()`) when it needs more pages of memory.

## free: Releasing Heap Memory

The `free()` function takes a pointer previously returned by `malloc()` and marks that memory as available for reuse:

```c
free(array);
```

Notice that `free()` does not take a size argument. The allocator tracks each allocation's size internally (typically in a header just before the returned pointer). This is why passing an invalid pointer to `free()` causes undefined behavior—the allocator reads garbage as size metadata.

## The System Calls Beneath

`malloc()` and `free()` are built on top of OS-provided system calls:

- **`brk()` / `sbrk()`**: Move the program break—the end of the heap segment. `sbrk(n)` extends the heap by `n` bytes. Simple but only allows growing/shrinking from the end.
- **`mmap()`**: Maps a region of virtual address space, optionally backed by a file or anonymous memory. Used by modern allocators for large allocations because mapped regions can be returned to the OS independently.

The allocator batches requests: rather than calling `sbrk()` for every `malloc()`, it requests a large chunk from the OS and carves it into smaller blocks internally. This amortizes the system call overhead.

## Library vs. System Call Distinction

This layering is important: `malloc()`/`free()` run entirely in user space most of the time. They maintain data structures (free lists, size headers) in the process's own heap. Only when the allocator's pool is exhausted does it [[System Calls Transfer Control via Trap and Return-from-Trap|trap into the kernel]] via `brk()` or `mmap()`. This design keeps allocation fast—a typical `malloc()` is just pointer arithmetic on a free list, not a context switch into the kernel.

## Why Manual Management

C provides no garbage collector. The programmer must explicitly free every allocated block when it is no longer needed. This gives maximum control and performance but introduces an entire category of [[Common Memory Bugs - Dangling Pointers Double Free and Leaks|memory bugs]] when discipline breaks down.
