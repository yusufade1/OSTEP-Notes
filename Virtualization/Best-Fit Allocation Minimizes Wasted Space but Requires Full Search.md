---
type: atomic
source: OSTEP Ch. 17
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation-strategy
related:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[Worst-Fit Allocation Leaves Large Holes but Still Fragments]]"
  - "[[First-Fit and Next-Fit Trade Search Time for Simplicity]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# Best-Fit Allocation Minimizes Wasted Space but Requires Full Search

> [!SUMMARY]
> Best-fit allocation searches the entire free list to find the smallest chunk that can satisfy a request, minimizing the leftover fragment from each allocation. While intuitively appealing, best-fit requires O(n) search time and can paradoxically increase fragmentation by creating many tiny unusable remnants.

## The Algorithm

Best-fit examines every free chunk and selects the one closest in size to the request:

```c
node_t *best_fit(int size) {
    node_t *curr = free_list;
    node_t *best = NULL;

    while (curr != NULL) {
        if (curr->size >= size) {
            if (best == NULL || curr->size < best->size) {
                best = curr;
            }
        }
        curr = curr->next;
    }
    return best;  // Returns NULL if no fit found
}
```

The algorithm cannot stop early—a perfect fit (or better fit) might exist later in the list.

## Worked Example

Request: 10 bytes

```
Free list: [20 bytes] → [15 bytes] → [12 bytes] → [30 bytes]

Best-fit search:
  20 >= 10? Yes, best candidate so far (20)
  15 >= 10? Yes, 15 < 20, new best (15)
  12 >= 10? Yes, 12 < 15, new best (12)
  30 >= 10? Yes, 30 > 12, keep best (12)

Result: Allocate from 12-byte chunk
        Leftover: 2 bytes (after header overhead)
```

## Trade-off Analysis

| Factor | Best-Fit Behavior |
|--------|-------------------|
| **Search time** | O(n) – must examine entire list |
| **Fragment size** | Minimizes per-allocation waste |
| **Fragmentation pattern** | Creates many tiny fragments |
| **Large allocation success** | Preserves large chunks (good) |

**The paradox**: By always choosing the tightest fit, best-fit leaves behind the smallest possible remnants. Over time, the free list accumulates many fragments too small to satisfy most requests. These "splinters" consume list space and slow searches without providing useful allocation capacity.

## When Best-Fit Works Well

Best-fit performs well when:
- Request sizes cluster around a few common values
- Coalescing frequently recombines fragments
- The overhead of full search is acceptable (small free list)

It performs poorly when:
- Request sizes vary widely (creates diverse splinter sizes)
- The free list grows large (search becomes expensive)
- Memory is tight (splinters cannot coalesce)

## Comparison to Other Strategies

Unlike [[First-Fit and Next-Fit Trade Search Time for Simplicity|first-fit]], best-fit cannot short-circuit its search. Unlike [[Worst-Fit Allocation Leaves Large Holes but Still Fragments|worst-fit]], it does not preserve large contiguous regions for future large requests. Best-fit optimizes for *individual* allocations at the potential cost of *system-wide* fragmentation—a local optimum that may not be globally optimal.

The fundamental insight is that minimizing per-allocation waste does not minimize total fragmentation. Real-world allocators often prefer first-fit or segregated fits over best-fit due to its search cost and fragmentation pathology.
