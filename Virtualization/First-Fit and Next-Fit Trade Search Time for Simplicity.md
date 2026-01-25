---
type: atomic
source: OSTEP Ch. 17
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation-strategy
related:
  - "[[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search]]"
  - "[[Worst-Fit Allocation Leaves Large Holes but Still Fragments]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# First-Fit and Next-Fit Trade Search Time for Simplicity

> [!SUMMARY]
> First-fit allocates from the first free chunk that is large enough, stopping the search immediately upon finding a fit. Next-fit is a variant that resumes searching from where the last allocation left off. Both achieve O(1) best-case and O(n) worst-case search time, but avoid the full-list scan that best-fit and worst-fit require. Despite their simplicity, these strategies often perform comparably to more sophisticated approaches.

## First-Fit Algorithm

First-fit returns the first chunk that satisfies the size requirement:

```c
node_t *first_fit(int size) {
    node_t *curr = free_list;

    while (curr != NULL) {
        if (curr->size >= size) {
            return curr;  // Found a fit, stop searching
        }
        curr = curr->next;
    }
    return NULL;  // No fit found
}
```

The key advantage is **early termination**: once a suitable chunk is found, search stops.

## Worked Example (First-Fit)

Request: 10 bytes

```
Free list: [8 bytes] → [15 bytes] → [12 bytes] → [30 bytes]

First-fit search:
  8 >= 10? No, continue
  15 >= 10? Yes → return this chunk

Result: Allocate from 15-byte chunk (search examined 2 of 4 chunks)
```

## Next-Fit Variant

Next-fit maintains a pointer to the last allocation position and starts searching from there:

```c
static node_t *last_position = NULL;

node_t *next_fit(int size) {
    node_t *start = (last_position != NULL) ? last_position : free_list;
    node_t *curr = start;

    do {
        if (curr->size >= size) {
            last_position = curr->next;
            return curr;
        }
        curr = curr->next;
        if (curr == NULL) curr = free_list;  // Wrap around
    } while (curr != start);

    return NULL;
}
```

The intuition: first-fit concentrates allocations at the beginning of the free list, potentially fragmenting the front while leaving the back pristine. Next-fit spreads allocations across the entire memory space.

## Trade-off Analysis

| Factor | First-Fit | Next-Fit |
|--------|-----------|----------|
| **Search time** | O(1) best, O(n) worst | O(1) best, O(n) worst |
| **Code complexity** | Minimal | Slightly more state |
| **Fragmentation location** | Front of list | Spread throughout |
| **Coalescing potential** | May preserve rear | More uniform fragmentation |

**Speed advantage**: Both avoid the mandatory full scan of [[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search|best-fit]] and [[Worst-Fit Allocation Leaves Large Holes but Still Fragments|worst-fit]]. For long free lists, this difference is substantial.

**Fragmentation behavior**: First-fit tends to fragment the beginning of memory while preserving larger chunks at the end. Next-fit fragments more uniformly. Neither is strictly better—the optimal choice depends on workload characteristics.

## Address-Ordered First-Fit

A refinement keeps the free list sorted by address. This enables efficient coalescing (neighbors are adjacent in list order) and can improve spatial locality. The trade-off is O(n) insertion time when freeing memory, versus O(1) for an unsorted list.

## Practical Relevance

First-fit remains competitive with sophisticated strategies in many workloads. Doug Lea's malloc (dlmalloc), one of the most influential allocators, uses first-fit within segregated size classes. The simplicity of first-fit means fewer bugs, faster path through the allocator, and predictable behavior—valuable properties in production systems.
