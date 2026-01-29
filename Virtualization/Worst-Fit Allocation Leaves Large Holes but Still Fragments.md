---
type: algorithm
source: "OSTEP Ch. 17: Free-Space Management"
tags:
  - virtualization
  - memory
  - free-space-management
  - allocation-strategy
related:
  - "[[Best-Fit Allocation Minimizes Wasted Space but Requires Full Search]]"
  - "[[First-Fit and Next-Fit Trade Search Time for Simplicity]]"
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[Splitting and Coalescing Keep the Free List Efficient]]"
  - "[[Virtualization MOC]]"
prerequisites:
  - "[[The Free List Data Structure Tracks Available Memory Regions]]"
  - "[[External Fragmentation Wastes Memory Between Variable-Sized Segments]]"
---

# Worst-Fit Allocation Leaves Large Holes but Still Fragments

> [!SUMMARY]
> Worst-fit allocation searches the entire free list for the largest available chunk and allocates from it. The rationale is that leaving large remainders (rather than tiny splinters) preserves usable free regions. In practice, worst-fit performs poorly—it still requires O(n) search time while fragmenting large chunks that could have satisfied big future requests.

## The Algorithm

Worst-fit is the inverse of best-fit:

```c
node_t *worst_fit(int size) {
    node_t *curr = free_list;
    node_t *worst = NULL;

    while (curr != NULL) {
        if (curr->size >= size) {
            if (worst == NULL || curr->size > worst->size) {
                worst = curr;
            }
        }
        curr = curr->next;
    }
    return worst;
}
```

Like best-fit, it must scan the entire list to find the maximum.

## Worked Example

Request: 10 bytes

```
Free list: [20 bytes] → [15 bytes] → [12 bytes] → [30 bytes]

Worst-fit search:
  20 >= 10? Yes, worst candidate so far (20)
  15 >= 10? Yes, 15 < 20, keep worst (20)
  12 >= 10? Yes, 12 < 20, keep worst (20)
  30 >= 10? Yes, 30 > 20, new worst (30)

Result: Allocate from 30-byte chunk
        Leftover: 20 bytes (after header overhead)
```

## Trade-off Analysis

| Factor | Worst-Fit Behavior |
|--------|-------------------|
| **Search time** | O(n) – must examine entire list |
| **Fragment size** | Leaves larger remnants |
| **Fragmentation pattern** | Breaks up large chunks quickly |
| **Large allocation success** | Rapidly consumes large regions (bad) |

**The problem**: Worst-fit's intuition—large leftovers are more useful—fails because it systematically attacks the large chunks first. After several allocations, no large contiguous regions remain. A subsequent request for a big allocation may fail even though total free memory is sufficient.

## Why Worst-Fit Underperforms

Consider a sequence of 10-byte allocations with initial free memory of one 100-byte chunk:

```
Initial:  [100]
After 1:  [90]   (worst-fit splits the only chunk)
After 2:  [80]
...
After 9:  [10]
After 10: empty

Now request 50 bytes → FAIL (no 50-byte region exists)
```

If instead we had multiple mid-sized chunks, worst-fit would still target the largest each time, reducing it until all chunks are similar in size—a uniform but potentially useless distribution.

## Comparison to Best-Fit

Both strategies require full list traversal (O(n)), so neither wins on search time. Best-fit creates tiny splinters; worst-fit erodes large chunks. Empirically, best-fit tends to outperform worst-fit on fragmentation metrics because small remnants occasionally coalesce, while destroyed large chunks are hard to reconstruct.

## Real-World Usage

Worst-fit is rarely used in production allocators. Its theoretical appeal (large leftovers should be useful) does not survive contact with real workloads. [[First-Fit and Next-Fit Trade Search Time for Simplicity|First-fit]] offers comparable fragmentation with faster search, and [[The Buddy System Enables Fast Coalescing Through Power-of-Two Sizes|buddy systems]] provide structured coalescing that worst-fit cannot match.

The lesson: intuitive allocation strategies may not produce intuitive results. Empirical measurement on representative workloads matters more than theoretical elegance.
