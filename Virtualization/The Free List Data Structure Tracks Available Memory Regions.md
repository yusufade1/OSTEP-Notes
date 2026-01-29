---
type: algorithm
source: "OSTEP Ch. 17: Free-Space Management"
tags:
  - virtualization
  - memory
  - free-space-management
  - data-structures
related:
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[The OS Manages Memory at Process Creation and Context Switch]]"
  - "[[First-Fit and Next-Fit Trade Search Time for Simplicity]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# The Free List Data Structure Tracks Available Memory Regions

> [!SUMMARY]
> The free list is a data structure that tracks all unallocated memory regions, enabling the allocator to find available space for new allocations and to reclaim freed memory. Typically implemented as a linked list embedded within the free memory itself, the free list is the foundation upon which allocation strategies like first-fit and best-fit operate.

## Basic Structure

The simplest free list is a singly-linked list of free chunks:

```c
typedef struct node_t {
    int size;           // Size of this free region
    struct node_t *next; // Pointer to next free region
} node_t;
```

The key insight is that **free memory can store its own metadata**. Since free regions are not in use, the allocator stores the node structure at the beginning of each free chunk:

```
Memory layout:
+----------------+-------------------+----------------+
| [size|next]    |   (unused space)  | [size|next]    | ...
| Free chunk 1   |                   | Free chunk 2   |
+----------------+-------------------+----------------+
```

This approach requires no separate metadata storage—the overhead is just the header bytes at the start of each free region.

## Operations

**Allocation search**: Walk the list to find a suitable chunk (criteria depend on the [[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search|allocation strategy]]). When found, either return the entire chunk or [[Splitting and Coalescing Keep the Free List Efficient|split]] it.

**Free and coalesce**: When memory is freed, create a new node for the returned region and add it to the list. Check for adjacent free regions to coalesce.

**List traversal**: Most operations require walking the list, making free list operations O(n) where n is the number of free chunks.

## Heap Growth and Initialization

When the heap is first initialized or needs more memory, the allocator requests space from the OS (via `sbrk` or `mmap`). The new region becomes a single large free chunk:

```c
// Initial heap: one chunk of heap_size bytes
free_list = (node_t *)heap_start;
free_list->size = heap_size - sizeof(node_t);
free_list->next = NULL;
```

As allocations and frees occur, this single chunk fragments into multiple entries on the free list.

## Embedded List Constraints

Embedding metadata in free memory means each free region must be at least `sizeof(node_t)` bytes. Requests smaller than this minimum cannot be satisfied without rounding up. Additionally, splitting creates overhead: a chunk of size S split to allocate R bytes leaves only `S - R - sizeof(node_t)` bytes in the remainder.

## Beyond Simple Lists

The basic linked list is simple but slow. Advanced allocators use more sophisticated structures:

- **Sorted lists**: Faster coalescing (neighbors are adjacent in list order) but slower insertion
- **Multiple lists (segregated lists)**: Separate lists for different size classes, reducing search time
- **Trees or bitmaps**: Faster search at the cost of complexity

These optimizations address the fundamental trade-off: simple data structures are easy to implement but slow; complex structures are faster but require more careful design. The [[The Buddy System Enables Fast Coalescing Through Power-of-Two Sizes|buddy system]] and [[Slab Allocators Pre-Allocate Fixed-Size Object Caches|slab allocator]] represent two influential approaches to this trade-off.
